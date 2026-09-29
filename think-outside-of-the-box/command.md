Build a ChatGPT Deep Research prompt from this project, not from memory.

**Arguments:** $ARGUMENTS

Invoke the Skill tool with `skill: "think-outside-of-the-box"`, passing `$ARGUMENTS`
through as `args`, and follow the workflow it returns.

Argument forms the skill understands:

- `<topic>` — the normal run
- `<topic> --anchor <path>` — override the project boundary
- `--result <path> [--slug S]` — file a returned Deep Research report
- `--list` — show recorded topics

Do not reimplement the workflow here. This file exists only so the command appears in the
slash menu; the skill at `~/.claude/skills/think-outside-of-the-box/` is the source of truth.
