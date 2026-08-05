#!/usr/bin/env python3
"""Turn a PDF book into per-chapter markdown, and lint the notes vault built from it.

Chapters come from the PDF's embedded outline (doc.get_toc()), not from a font-size
heuristic: measured on two real books, no single font-scale default serves both.
Ernie Chan's section heads sit at 1.33x body size, so the obvious 1.4 default rejects
every one of them, while Irene Aldridge's candidate count barely moves across 1.15-1.5.

Source of truth for this file is scripts/book-atomizer/booknotes.py in the Backtesting
repo. The copy at ~/.claude/skills/book-atomizer/booknotes.py is deployed from here;
re-copy after editing.

Usage:
    booknotes.py probe <book.pdf>
    booknotes.py split <book.pdf> [--out DIR] [--split-regex RX] [--force]
    booknotes.py index <vault-dir>
    booknotes.py lint  <vault-dir>
    booknotes.py --demo
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FITZ_HELP = "PyMuPDF is required: pip install pymupdf"

try:
    import fitz
except ImportError:  # pragma: no cover - exercised by demo group 1's message check
    print(FITZ_HELP)
    sys.exit(1)

# ponytail: copy of docx_to_md.slug(), keep in sync. Demo group 6 asserts byte-identity
# against that file when it is reachable from cwd.
_TR = str.maketrans("şŞıİğĞüÜöÖçÇ", "sSiIgGuUoOcC")


def slug(stem):
    s = stem.translate(_TR)
    s = re.sub(r"['’`]", "", s)
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


# ---------------------------------------------------------------- PDF reading

_CODEISH = re.compile(r"(^\s{4,}\w|;\s*$|\b(function|for\s*\(|end;|import |def )\b)")

EDGE_TOP = 0.08
EDGE_BOTTOM = 0.92
# Measured, not guessed: Aldridge's running head sits on 38.4% of pages and Chan has no
# recurrent edge line at all, so >60% (rev 2) fires on neither book and >30% fires only
# on Aldridge. 25% catches Aldridge and stays quiet on Chan.
EDGE_SHARE = 0.25


def _lines(doc):
    """(page_index, y_ratio, dominant_size, text, lines_in_block) for every non-empty line."""
    out = []
    for pno, page in enumerate(doc):
        height = page.rect.height or 1.0
        for block in page.get_text("dict")["blocks"]:
            blines = block.get("lines", [])
            for line in blines:
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                text = "".join(s["text"] for s in line["spans"]).strip()
                if not text:
                    continue
                dominant = max(spans, key=lambda s: len(s["text"].strip()))
                out.append((pno, line["bbox"][1] / height, round(dominant["size"], 1),
                            text, len(blines)))
    return out


def _norm_edge(text):
    return re.sub(r"\d+", "", text).strip().lower()


def _is_edge(y_ratio):
    return y_ratio < EDGE_TOP or y_ratio > EDGE_BOTTOM


def probe_pdf(doc):
    """Measurements the split stage and the operator both need. Pure read, no writes.

    chars/chars_per_page count STRIPPED SPAN text. Any other basis (whole-line text,
    raw page.get_text()) gives a different number for the same book; do not mix them.
    """
    lines = _lines(doc)
    pages = len(doc) or 1

    size_chars = collections.Counter()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    t = span["text"].strip()
                    if t:
                        size_chars[round(span["size"], 1)] += len(t)

    chars = sum(size_chars.values())
    body = size_chars.most_common(1)[0][0] if size_chars else 0.0
    total = chars or 1
    buckets = [[sz, round(100.0 * c / total, 2)] for sz, c in size_chars.most_common(5)]

    dropcaps = sum(1 for _, _, sz, t, _ in lines if body and sz >= 1.4 * body and len(t) <= 2)

    edge = collections.Counter(
        _norm_edge(t) for _, yr, _, t, _ in lines if _is_edge(yr) and _norm_edge(t)
    )
    edge_lines = sorted(([t, round(c / pages, 4)] for t, c in edge.items()
                         if c / pages > EDGE_SHARE), key=lambda r: -r[1])

    codeish = sum(1 for _, _, _, t, _ in lines if _CODEISH.search(t))
    code_share = codeish / len(lines) if lines else 0.0

    return {
        "pages": len(doc),
        "chars": chars,
        "chars_per_page": round(chars / pages, 1),
        "has_text_layer": chars / pages >= 100,
        "body_size": body,
        "size_buckets": buckets,
        "outline_entries": len(doc.get_toc()),
        "dropcaps": dropcaps,
        "edge_lines": edge_lines,
        "code_share": round(code_share, 4),
        "has_code": code_share > 0.02,
    }


# ---------------------------------------------------------------- chapters

_CHAPTER_RX = re.compile(r"^\s*chapter\s+\d+", re.I)


def find_chapters(doc):
    """Chapters from the PDF's embedded outline.

    Primary rule: outline entries matching '^chapter N' at ANY level, if >=3 match.
    Aldridge nests chapters at level 2 under a level-1 book title while Chan puts them
    at level 1, so keying on the level would need per-book tuning; keying on the title
    text does not.

    Fallback: the shallowest level with >=3 entries.

    The last chapter is clamped to the first following entry at level <= its own,
    otherwise it absorbs the back matter (measured: Chan's chapter 8 ran to p226
    swallowing CONCLUSION/BIBLIOGRAPHY/INDEX; Aldridge's chapter 19 ran to p358
    swallowing References/Index).

    page_start is 1-based inclusive, page_end is 1-based EXCLUSIVE: the chapter's text
    is doc[i] for i in range(page_start - 1, page_end - 1).
    """
    toc = doc.get_toc()
    if not toc:
        return [], "none"

    hits = [(i, t) for i, t in enumerate(toc) if _CHAPTER_RX.match(t[1])]
    rule = "outline: ^chapter N"
    if len(hits) < 3:
        hits, rule = [], "outline: shallowest level with >=3 entries"
        for level in sorted({t[0] for t in toc}):
            at_level = [(i, t) for i, t in enumerate(toc) if t[0] == level]
            if len(at_level) >= 3:
                hits = at_level
                break
    if len(hits) < 3:
        return [], "none"

    npages = len(doc)
    chapters = []
    for k, (idx, entry) in enumerate(hits):
        level, title, page = entry[0], entry[1], entry[2]
        if k + 1 < len(hits):
            end = hits[k + 1][1][2]
        else:
            following = [t for t in toc[idx + 1:] if t[0] <= level]
            end = following[0][2] if following else npages + 1
        chapters.append({"n": k + 1, "title": title.strip(),
                         "page_start": page, "page_end": end})
    return chapters, rule


def _chapters_by_regex(doc, rx):
    pat = re.compile(rx)
    starts = []
    for pno, _, _, text, _ in _lines(doc):
        if pat.match(text) and (not starts or starts[-1][0] != pno + 1):
            starts.append((pno + 1, text.strip()))
    if not starts:
        return []
    out = []
    for k, (page, title) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(doc) + 1
        out.append({"n": k + 1, "title": title, "page_start": page, "page_end": end})
    return out


# ---------------------------------------------------------------- commands

def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_probe(path):
    doc = fitz.open(path)
    pr = probe_pdf(doc)
    chapters, rule = find_chapters(doc)
    print(f"{os.path.basename(path)}")
    print(f"  pages={pr['pages']}  chars={pr['chars']}  chars/page={pr['chars_per_page']}"
          f"  text_layer={'YES' if pr['has_text_layer'] else 'NO'}")
    print(f"  modal body size = {pr['body_size']}  (stripped-span char-weighted mode, 1dp)")
    for sz, share in pr["size_buckets"]:
        ratio = sz / pr["body_size"] if pr["body_size"] else 0
        print(f"     {sz:6}  {share:5.2f}%  ratio_to_body={ratio:.2f}")
    print(f"  outline entries = {pr['outline_entries']}")
    print(f"  chapters = {len(chapters)} via {rule}")
    for c in chapters:
        span = c["page_end"] - c["page_start"]
        print(f"     {c['n']:02d}  p{c['page_start']}-{c['page_end'] - 1} ({span}p)"
              f"  {c['title'][:52]}")
    print(f"  drop-cap-shaped lines = {pr['dropcaps']}")
    print(f"  recurrent edge lines (>{int(EDGE_SHARE * 100)}% of pages) = {len(pr['edge_lines'])}")
    for t, share in pr["edge_lines"]:
        print(f"     {100 * share:5.1f}%  {t[:60]!r}")
    print(f"  code share = {100 * pr['code_share']:.1f}%  has_code={pr['has_code']}")
    doc.close()
    return 0


def cmd_split(pdf_path, out_dir, split_regex, force):
    doc = fitz.open(pdf_path)
    pr = probe_pdf(doc)

    if not pr["has_text_layer"]:
        print(f"this PDF has no text layer (avg {pr['chars_per_page']} chars/page); "
              f"scanned PDFs are out of scope")
        doc.close()
        return 2

    chapters, rule = find_chapters(doc)
    if not chapters and split_regex:
        chapters = _chapters_by_regex(doc, split_regex)
        rule = f"regex: {split_regex}"
    if not chapters:
        print("no embedded outline and no --split-regex. Largest-font candidate lines:")
        body = pr["body_size"] or 1
        for pno, _, size, text, _ in [l for l in _lines(doc) if l[2] >= 1.2 * body][:5]:
            print(f"   p{pno + 1} size={size} {text[:60]!r}")
        print("re-run with --split-regex PATTERN")
        doc.close()
        return 3

    raw_dir = os.path.join(out_dir, "raw")
    if os.path.isdir(raw_dir) and os.listdir(raw_dir) and not force:
        print(f"{raw_dir} already contains:")
        for name in sorted(os.listdir(raw_dir)):
            print(f"   {name}")
        print("re-run with --force to rewrite raw/ (notes/ is never touched)")
        doc.close()
        return 4
    os.makedirs(raw_dir, exist_ok=True)
    for name in os.listdir(raw_dir):
        target = os.path.join(raw_dir, name)
        if os.path.isfile(target):
            os.remove(target)

    # Both drops are gated on the edge zone. Dropping recurrent text at ANY y amputates
    # real content: 4 of Aldridge's 141 'high-frequency trading' lines are mid-body, one
    # inside a Sharpe-ratio formula caption. Dropping every all-digit line at any y
    # destroys 309 lines in Chan that are not page numbers.
    drop = {t for t, _ in pr["edge_lines"]}
    by_page = collections.defaultdict(list)
    for pno, yr, _, text, _ in _lines(doc):
        by_page[pno].append((yr, text))

    book = os.path.splitext(os.path.basename(pdf_path))[0]
    today = date.today().isoformat()

    for ch in chapters:
        kept = []
        for pno in range(ch["page_start"] - 1, min(ch["page_end"] - 1, len(doc))):
            for yr, text in by_page.get(pno, []):
                if _is_edge(yr) and (_norm_edge(text) in drop or re.fullmatch(r"\d+", text)):
                    continue
                kept.append(text)
            kept.append("")
        body_text = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()
        ch["chars"] = len(body_text)

        # The number prefix is required: Aldridge's chapters 10 and 11 share a title.
        name = f"ch{ch['n']:02d}-{slug(ch['title'])}.md"
        front = (
            "---\n"
            f'book: "{book}"\n'
            f'chapter: "{ch["n"]:02d} — {ch["title"]}"\n'
            f'pages: "{ch["page_start"]}-{ch["page_end"] - 1}"\n'
            f'source_pdf: "{os.path.basename(pdf_path)}"\n'
            f"converted: {today}\n"
            "---\n\n"
        )
        with open(os.path.join(raw_dir, name), "w", encoding="utf-8") as fh:
            fh.write(front + f"# {ch['title']}\n\n" + body_text + "\n")

    manifest = {
        "book": book,
        "source_path": os.path.abspath(pdf_path),
        "source_sha256": _sha256(pdf_path),
        "chapter_rule": rule,
        "chapters": chapters,
        "has_code": pr["has_code"],
        "probe": pr,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)

    doc.close()
    print(f"{len(chapters)} chapters via {rule} -> {raw_dir}")
    return 0


# ---------------------------------------------------------------- vault

INDEX_START = "<!-- booknotes:index:start -->"
INDEX_END = "<!-- booknotes:index:end -->"


def _frontmatter(path):
    """(frontmatter dict, body text after the --- block)."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return out, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out, text[m.end():]


def build_index(vault):
    paths = sorted(glob.glob(os.path.join(vault, "notes", "*.md")))
    rows = []
    for p in paths:
        fm, _ = _frontmatter(p)
        stem = os.path.splitext(os.path.basename(p))[0]
        rows.append((stem, fm.get("title", stem), fm.get("chapter", "?")))

    lines = [
        "# Index", "",
        "Generated. Do not hand-edit anything between the sentinels.", "",
        "```", "python $BA index <this directory>", "```", "",
        INDEX_START, "",
        f"{len(rows)} notes", "",
        "| note | title | chapter |",
        "|---|---|---|",
    ]
    for stem, title, chapter in rows:
        lines.append(f"| `{stem}` | {title} | {chapter} |")
    lines += ["", INDEX_END, ""]

    with open(os.path.join(vault, "index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"index: {len(rows)} notes -> {os.path.join(vault, 'index.md')}")
    return 0


REQUIRED_KEYS = ("provenance", "verification", "book", "chapter")
# Counts OF OUR OWN MATERIAL. A number quoted from the book is legal and must sit in a
# blockquote. Copying docs/wiki's blanket "no digit" rule here would forbid the 2.5 R/K
# note, which is the one the wiki actually wants.
OWN_COUNT_RX = re.compile(r"\b\d[\d.,]*\s+(notes?|chapters?|pages?|concepts?|sources?|rows?)\b",
                          re.I)
WIKILINK_RX = re.compile(r"\[\[([^\]]+)\]\]")
GATE_RX = re.compile(r"^\(a\) \S+:\d+$|^\(b\) owner \d{4}-\d{2}-\d{2}$")


def _strip_code(text):
    """Blank out fenced blocks and inline code spans, preserving line count.

    docs/wiki/CLAUDE.md warns whoever writes this lint: v1's drift checker had to choose
    between parsing code spans and failing loud on its own documentation. Parse them.
    """
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else re.sub(r"`[^`]*`", "", line))
    return out


def _gate_rows(vault):
    path = os.path.join(vault, "plan.md")
    rows = {}
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[0] not in ("note",) and not set(cells[0]) <= {"-"}:
                rows[cells[0]] = cells[2]
    return rows


def lint_vault(vault):
    """Rule 3 resolves a cited (a) path relative to the PROCESS cwd, not the vault.

    That is deliberate: the citation points into the project's knowledge layer
    (FINDINGS.md, docs/knowledgebase/...), which is addressed from the repo root, and
    lint is documented as being run from the repo root.
    """
    findings = []
    notes = sorted(glob.glob(os.path.join(vault, "notes", "*.md")))
    stems = {os.path.splitext(os.path.basename(p))[0] for p in notes}
    gates = _gate_rows(vault)

    for path in notes:
        stem = os.path.splitext(os.path.basename(path))[0]
        fm, body = _frontmatter(path)

        missing = [k for k in REQUIRED_KEYS if not fm.get(k)]
        if missing:
            findings.append(f"{path}: rule 1 - missing frontmatter {', '.join(missing)}")

        for i, line in enumerate(_strip_code(body), 1):
            for target in WIKILINK_RX.findall(line):
                if target.split("|")[0].strip() not in stems:
                    findings.append(
                        f"{path}:{i}: rule 2 - wikilink [[{target}]] resolves to nothing")
            if not line.lstrip().startswith(">") and OWN_COUNT_RX.search(line):
                findings.append(f"{path}:{i}: rule 4 - hand-typed count of our own material")

        gate = gates.get(stem)
        if not gate:
            findings.append(f"{path}: rule 3 - no gate row in plan.md")
        elif not GATE_RX.match(gate):
            findings.append(
                f"{path}: rule 3 - gate cell {gate!r} is not (a) path:line or (b) owner DATE")
        elif gate.startswith("(a)"):
            cited = gate[4:].rsplit(":", 1)[0]
            if not os.path.exists(cited):
                findings.append(f"{path}: rule 3 - cited artifact {cited} does not exist")

    index = os.path.join(vault, "index.md")
    if os.path.exists(index):
        with open(index, encoding="utf-8") as fh:
            text = fh.read()
        if INDEX_START in text and INDEX_END in text:
            outside = text.split(INDEX_START)[0] + text.split(INDEX_END)[-1]
        else:
            outside = text
        if re.search(r"\d", outside):
            findings.append(f"{index}: rule 5 - digit outside the generated block")

    man_path = os.path.join(vault, "manifest.json")
    if os.path.exists(man_path):
        with open(man_path, encoding="utf-8") as fh:
            man = json.load(fh)
        if any(_frontmatter(p)[0].get("provenance") == "RELAY" for p in notes):
            src = man.get("source_path", "")
            if not os.path.exists(src):
                findings.append(
                    f"rule 6 - source PDF missing at {src}; every note must become ORPHAN")
            elif _sha256(src) != man.get("source_sha256"):
                findings.append(
                    "rule 6 - source PDF sha mismatch; every note must become ORPHAN")

    for f in findings:
        print(f)
    print(f"lint: {len(findings)} finding(s)")
    return 1 if findings else 0


# ---------------------------------------------------------------- self-check

_FAILURES = []


def _check(cond, label):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        _FAILURES.append(label)


def _page(doc, texts, size=11):
    """A page carrying enough text to clear the 100 chars/page text-layer guard.

    PyMuPDF's default font is WinAnsi and silently mangles 'ı' and '∑'
    ('kılıfına' -> 'k·l·f·na'), so synthetic PDFs use WinAnsi-safe non-ASCII only.
    The real utf-8 path is asserted on file I/O in group 8.
    """
    pg = doc.new_page()
    for j, t in enumerate(texts):
        pg.insert_text((72, 100 + 14 * j), t, fontsize=size)
    return pg


_FILLER = ["café résumé Ünlü body prose line one here",
           "second filler line of ordinary body prose",
           "third filler line of ordinary body prose",
           "fourth filler line of ordinary body prose"]


def demo():
    tmp = tempfile.mkdtemp(prefix="booknotes-demo-")

    print("group 1: import guard")
    _check(FITZ_HELP == "PyMuPDF is required: pip install pymupdf",
           "install message is the exact documented string")

    print("group 6: slug")
    _check(slug("Ali Perşembe_s Strategic Framework") == "ali-persembe-s-strategic-framework",
           "slug folds Turkish and strips punctuation")
    _check(slug("The GSL List_ Nine Pillars") == "the-gsl-list-nine-pillars",
           "slug handles the underscore-colon case")
    _check(slug("Chapter 19: Post-Trade Profitability Analysis")
           == "chapter-19-post-trade-profitability-analysis",
           "slug handles a real chapter title")
    src = os.path.join("scripts", "utils", "docx_to_md.py")
    if os.path.exists(src):
        pat = r"^def slug\(stem\):\n(?:.*\n)*?^    return .*$"
        with open(src, encoding="utf-8") as fh:
            theirs = re.search(pat, fh.read(), re.M)
        with open(__file__, encoding="utf-8") as fh:
            mine = re.search(pat, fh.read(), re.M)
        _check(bool(theirs) and bool(mine) and theirs.group(0) == mine.group(0),
               "slug() is byte-identical to docx_to_md.slug()")
    else:
        print("  SKIP  slug-drift (docx_to_md.py not reachable from cwd)")

    print("group 4: probe")
    img = fitz.open()
    page = img.new_page()
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 50, 50))
    pix.set_rect(pix.irect, (200, 10, 10))
    page.insert_image(fitz.Rect(50, 50, 200, 200), pixmap=pix)
    p_img = os.path.join(tmp, "img_only.pdf")
    img.save(p_img)
    img.close()
    d = fitz.open(p_img)
    pr = probe_pdf(d)
    d.close()
    _check(pr["has_text_layer"] is False, "image-only PDF reports no text layer")
    _check(pr["chars"] == 0, "image-only PDF extracts zero characters")

    txt = fitz.open()
    for _ in range(3):
        _page(txt, _FILLER)
    p_txt = os.path.join(tmp, "text.pdf")
    txt.save(p_txt)
    txt.close()
    d = fitz.open(p_txt)
    pr = probe_pdf(d)
    d.close()
    _check(pr["has_text_layer"] is True, "text PDF reports a text layer")
    _check(pr["body_size"] == 11.0, "modal body size is the char-weighted mode at 1dp")
    _check(pr["edge_lines"] == [], "no recurrent edge line on a plain PDF")
    _check(pr["has_code"] is False, "prose PDF is not flagged as containing code")

    hdr = fitz.open()
    for i in range(3):
        pg = hdr.new_page()
        if i < 2:  # 2 of 3 pages = 0.67, above the 0.25 threshold
            pg.insert_text((72, 12), "Running Head Of The Book", fontsize=9)
        for j, t in enumerate(_FILLER):
            pg.insert_text((72, 100 + 14 * j), t, fontsize=11)
    p_hdr = os.path.join(tmp, "hdr.pdf")
    hdr.save(p_hdr)
    hdr.close()
    d = fitz.open(p_hdr)
    pr = probe_pdf(d)
    d.close()
    _check(len(pr["edge_lines"]) == 1 and pr["edge_lines"][0][0] == "running head of the book",
           "a header on 2 of 3 pages clears the >25% threshold")

    print("group 2: chapters from the embedded outline")
    book = fitz.open()
    for i in range(6):
        _page(book, [f"body page {i} café"] + _FILLER)
    book.set_toc([[1, "Front Matter", 1],
                  [1, "Chapter 1: Alpha", 2],
                  [1, "Chapter 2: Beta", 4],
                  [1, "Chapter 3: Gamma", 5],
                  [1, "Index", 6]])
    p_book = os.path.join(tmp, "book.pdf")
    book.save(p_book)
    book.close()
    d = fitz.open(p_book)
    chapters, rule = find_chapters(d)
    d.close()
    _check(len(chapters) == 3, "three chapters detected, front matter excluded")
    _check(rule == "outline: ^chapter N", "the ^chapter N rule was the one that fired")
    _check(chapters[0]["title"] == "Chapter 1: Alpha", "title comes from the outline verbatim")
    _check(chapters[0]["page_start"] == 2 and chapters[0]["page_end"] == 4,
           "chapter 1 spans pages 2..3 (end exclusive)")

    print("group 5: back-matter clamp")
    _check(chapters[-1]["page_end"] == 6, "last chapter ends at Index, not end-of-document")

    print("group 3: no outline and no --split-regex")
    flat = fitz.open()
    for i in range(3):
        _page(flat, [f"uniform body text {i}"] + _FILLER)
    p_flat = os.path.join(tmp, "flat.pdf")
    flat.save(p_flat)
    flat.close()
    d = fitz.open(p_flat)
    chapters_flat, rule_flat = find_chapters(d)
    d.close()
    _check(chapters_flat == [] and rule_flat == "none", "a PDF with no outline yields no chapters")

    print("group 7: split")
    out = os.path.join(tmp, "vault")
    _check(cmd_split(p_book, out, None, False) == 0, "split succeeds on a PDF with an outline")
    raw = sorted(os.listdir(os.path.join(out, "raw")))
    _check(raw == ["ch01-chapter-1-alpha.md", "ch02-chapter-2-beta.md",
                   "ch03-chapter-3-gamma.md"], "chapter files are numbered and slugged")
    with open(os.path.join(out, "manifest.json"), encoding="utf-8") as fh:
        man = json.load(fh)
    _check(len(man["chapters"]) == 3, "manifest lists three chapters")
    _check(len(man.get("source_sha256", "")) == 64, "manifest carries a sha256 of the source")
    _check(os.path.isabs(man["source_path"]), "manifest carries an absolute source path")
    _check(cmd_split(p_book, out, None, False) != 0,
           "re-running without --force refuses and exits non-zero")
    _check(cmd_split(p_img, os.path.join(tmp, "v2"), None, False) == 2,
           "an image-only PDF is rejected by the text-layer guard")
    _check(cmd_split(p_flat, os.path.join(tmp, "v3"), None, False) == 3,
           "no outline and no --split-regex exits non-zero")
    _check(cmd_split(p_flat, os.path.join(tmp, "v4"), r"^uniform body text \d", False) == 0,
           "--split-regex rescues a PDF with no outline")

    print("group 8: utf-8 file round-trip")
    u8 = os.path.join(tmp, "u8.md")
    payload = "kılıfına uydurma ∑ emniyet yastığı"
    with open(u8, "w", encoding="utf-8") as fh:
        fh.write(payload)
    with open(u8, encoding="utf-8") as fh:
        _check(fh.read() == payload, "utf-8 write/read round-trips Turkish and math glyphs")

    print("group 9: index")
    notes = os.path.join(out, "notes")
    os.makedirs(notes, exist_ok=True)
    for title, chap in [("Alpha Concept", "01 — Chapter 1: Alpha"),
                        ("Beta Concept", "02 — Chapter 2: Beta")]:
        with open(os.path.join(notes, slug(title) + ".md"), "w", encoding="utf-8") as fh:
            fh.write(f'---\ntitle: "{title}"\nbook: "Demo Book"\nchapter: "{chap}"\n'
                     f"provenance: RELAY\nverification: UNTESTED\n---\n\n# {title}\n")
    _check(build_index(out) == 0, "index exits 0")
    with open(os.path.join(out, "index.md"), encoding="utf-8") as fh:
        body = fh.read()
    _check("2 notes" in body, "index reports the note count read from disk")
    _check(INDEX_START in body and INDEX_END in body, "index wraps its block in sentinels")
    _check("alpha-concept" in body and "beta-concept" in body, "index lists every note")

    print("group 7b: --force never touches notes/")
    before = sorted(os.listdir(notes))
    _check(cmd_split(p_book, out, None, True) == 0, "--force rewrites raw/")
    _check(sorted(os.listdir(notes)) == before and before,
           "notes/ is untouched by --force")
    build_index(out)

    print("group 10: lint")
    plan_path = os.path.join(out, "plan.md")

    def write_plan(alpha_gate):
        with open(plan_path, "w", encoding="utf-8") as fh:
            fh.write("| note | chapter | gate |\n|---|---|---|\n"
                     f"| alpha-concept | 01 | {alpha_gate} |\n"
                     "| beta-concept | 02 | (b) owner 2026-07-31 |\n")

    # Cite a path that cannot exist under ANY cwd, so the assertion does not depend on
    # whether the ambient working directory happens to contain a real FINDINGS.md.
    write_plan("(a) no-such-artifact-e3f1a9.md:12")
    _check(lint_vault(out) != 0, "lint fails when the cited artifact does not exist")
    write_plan("(a) beta-concept-cite.md:12")
    with open(os.path.join(out, "beta-concept-cite.md"), "w", encoding="utf-8") as fh:
        fh.write("cited artifact\n")

    cwd = os.getcwd()
    os.chdir(out)
    try:
        _check(lint_vault(".") == 0, "a clean vault passes")

        alpha = os.path.join("notes", "alpha-concept.md")
        with open(alpha, "a", encoding="utf-8") as fh:
            fh.write("\n> The author reports 3 chapters of results.\n")
        _check(lint_vault(".") == 0,
               "a count quoted from the book inside a blockquote is legal")
        with open(alpha, "a", encoding="utf-8") as fh:
            fh.write("\nThis vault holds 2 notes so far.\n")
        _check(lint_vault(".") != 0, "the same shape outside a blockquote fails")
        os.remove(alpha)
        build_index(".")

        gamma = os.path.join("notes", "gamma-concept.md")
        with open(gamma, "w", encoding="utf-8") as fh:
            fh.write('---\ntitle: "Gamma"\nprovenance: RELAY\n---\n\n# Gamma\n')
        _check(lint_vault(".") != 0, "a note missing verification/book/chapter fails")
        os.remove(gamma)
        build_index(".")

        beta = os.path.join("notes", "beta-concept.md")
        with open(beta, "a", encoding="utf-8") as fh:
            fh.write("\nSee `[[nowhere]]` in a code span, fine.\n")
        _check(lint_vault(".") == 0, "a dead wikilink inside a code span is ignored")
        with open(beta, "a", encoding="utf-8") as fh:
            fh.write("\n```\n[[also-nowhere]]\n```\n")
        _check(lint_vault(".") == 0, "a dead wikilink inside a fenced block is ignored")
        with open(beta, "a", encoding="utf-8") as fh:
            fh.write("\nSee [[nowhere]] outside one.\n")
        _check(lint_vault(".") != 0, "a dead wikilink outside code fails")
    finally:
        os.chdir(cwd)

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{'DEMO PASS' if not _FAILURES else 'DEMO FAIL: ' + '; '.join(_FAILURES)}")
    return 1 if _FAILURES else 0


def main():
    ap = argparse.ArgumentParser(prog="booknotes.py")
    ap.add_argument("--demo", action="store_true",
                    help="self-check, writes nothing outside a temp dir")
    sub = ap.add_subparsers(dest="cmd")

    p_probe = sub.add_parser("probe")
    p_probe.add_argument("pdf")

    p_split = sub.add_parser("split")
    p_split.add_argument("pdf")
    p_split.add_argument("--out")
    p_split.add_argument("--split-regex", dest="split_regex")
    p_split.add_argument("--force", action="store_true")

    sub.add_parser("index").add_argument("vault")
    sub.add_parser("lint").add_argument("vault")

    args = ap.parse_args()
    if args.demo:
        return demo()
    if args.cmd == "probe":
        return cmd_probe(args.pdf)
    if args.cmd == "split":
        out = args.out or os.path.join(
            "docs", "booknotes", slug(os.path.splitext(os.path.basename(args.pdf))[0]))
        return cmd_split(args.pdf, out, args.split_regex, args.force)
    if args.cmd == "index":
        return build_index(args.vault)
    if args.cmd == "lint":
        return lint_vault(args.vault)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
