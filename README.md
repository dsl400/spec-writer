# spec-writer

A skill for Claude Code that writes specifications in ASD-STE100, with EARS
requirements and RFC 2119 obligation words, and checks each file with the
`ste-check` tool that it holds.

## Contents

- `SKILL.md` — the skill.
- `tools/ste/ste-check` — the ASD-STE100 checker. It reads `wordset.json`
  next to it and `<workspace>/docs/project-terms.txt`.
- `tools/ste/test_ste_check.py` — the tests of the checker.

## Install

```sh
git clone git@github.com:dsl400/spec-writer.git ~/.claude/skills/spec-writer
```

For one project only, clone it into `<project>/.claude/skills/spec-writer`.

## Test

```sh
python3 -m pytest tools/ste
```
