# spec-writer

Two skills for Claude Code, delivered as one package:

- `spec-writer` writes requirement specifications under `docs/reference/` in
  ASD-STE100, with EARS triggers and RFC 2119 obligation words, and checks each
  file with the `ste-check` tool that it holds.
- `spec-extractor` reads the application and writes the functional specs of
  its screens under `docs/specs/`. It files the gaps it finds as GitHub issues
  and checks each file with the check of `spec-writer`.

## Contents

- `skills/spec-writer/SKILL.md` — the spec-writer skill.
- `skills/spec-extractor/SKILL.md` — the spec-extractor skill.
- `skills/spec-writer/tools/ste/ste-check` — the ASD-STE100 checker. It reads `wordset.json`
  next to it and `<workspace>/docs/project-terms.txt`.
- `skills/spec-writer/tools/ste/test_ste_check.py` — the tests of the checker.

## Install

Each release holds `spec-writer.tar.gz` with both skills. Each `SKILL.md` names the source
repository and the version of the release (`metadata.source`,
`metadata.version`); the release workflow writes the version from the tag.

```sh
gh release download --repo dsl400/spec-writer --pattern spec-writer.tar.gz -O - | tar -xz -C ~/.claude/skills
```

Or from the source:

```sh
git clone git@github.com:dsl400/spec-writer.git
ln -s "$PWD/spec-writer/skills/spec-writer" ~/.claude/skills/spec-writer
ln -s "$PWD/spec-writer/skills/spec-extractor" ~/.claude/skills/spec-extractor
```

For one project only, link both into `<project>/.claude/skills/`.

## Test

```sh
python3 -m pytest skills/spec-writer/tools/ste
```
