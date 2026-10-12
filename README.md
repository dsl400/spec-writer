# spec-writer

A skill for Claude Code that writes specifications in ASD-STE100, with EARS
requirements and RFC 2119 obligation words, and checks each file with the
`ste-check` tool that it holds.

## Contents

- `skills/spec-writer/SKILL.md` — the skill.
- `skills/spec-writer/tools/ste/ste-check` — the ASD-STE100 checker. It reads `wordset.json`
  next to it and `<workspace>/docs/project-terms.txt`.
- `skills/spec-writer/tools/ste/test_ste_check.py` — the tests of the checker.

## Install

Each release holds `spec-writer.tar.gz`. Its `SKILL.md` names the source
repository and the version of the release (`metadata.source`,
`metadata.version`); the release workflow writes the version from the tag.

```sh
gh release download --repo dsl400/spec-writer --pattern spec-writer.tar.gz -O - | tar -xz -C ~/.claude/skills
```

Or from the source:

```sh
git clone git@github.com:dsl400/spec-writer.git
ln -s "$PWD/spec-writer/skills/spec-writer" ~/.claude/skills/spec-writer
```

For one project only, link it into `<project>/.claude/skills/spec-writer`.

## Test

```sh
python3 -m pytest skills/spec-writer/tools/ste
```
