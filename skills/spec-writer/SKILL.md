---
name: spec-writer
description: Use when the user asks to write, change, or review a specification (specificație) under docs/reference/. Writes each requirement in EARS with RFC 2119 obligation words, in ASD-STE100, and checks each file with the ste-check tool that comes with this skill.
user-invocable: true
metadata:
  source: https://github.com/dsl400/spec-writer
  version: 0.1.0
---

# Spec Writer

A specification states what the application must do: the behavior and its
result.

`<skill>` is the folder of this file. `<workspace>` is the root of the project
that holds `docs/`.

## The index of the specifications

`<workspace>/docs/reference/README.md` holds the exemplar and the prefix
table of the project:

```markdown
# Specifications

Exemplar: `01-harness.md`

| Prefix | Specification |
| --- | --- |
| `APP` | `00-app.md` |
| `HRS` | `01-harness.md` |
```

- The exemplar is the specification that each new file copies the shape of.
- IF the index is absent, THEN create it from the files of `docs/reference/`
  and name the most complete file as the exemplar.

## The shape of a file

A specification holds these parts, in this order:

- **The title**: `# <NN> — <Subject>`. `<NN>` is the number of the file.
- **The principle**: the idea of the specification, in prose. Add a code
  block that shows the shape when a shape exists.
- **The requirements**: a list of requirement items.
- **The verification**: the document, the trace, or the test that shows that
  the requirements hold.

## The requirement item

```markdown
- **CTX-11** — WHEN the model operates the `context` tool, the harness must
  apply `exclude` to each earlier use of that tool. The record keeps all of
  those lines, so the file stays full.
```

- The first sentence holds the trigger and the obligation word.
- A sentence after it holds the reason.
- The trigger takes EARS syntax: `WHEN <event>`, `WHILE <condition>`,
  `WHERE <feature>`, `IF <condition>, THEN`, or no trigger for a rule that
  is always true.
- The obligation takes RFC 2119: `must`, `must not`, `should`, `may`. STE
  rejects `shall`, and RFC 2119 gives `must` the same force.

## The identifier

Each specification has one prefix of three letters. The prefix and a number
make the identifier of a requirement. The identifier stays with its
requirement for the life of the project.

- A new requirement gets the number after the highest number in use.
- A requirement that you remove keeps its number retired. No requirement
  uses that number again.
- A new specification adds its prefix to the table of the index.

## A requirement is complete alone

A reader understands a requirement with no other page open. The requirement
names in words each thing it uses. WHEN the reader needs the definition of
such a thing, the sentence ends with the identifier of that definition in
parentheses. The sentence is complete when you remove the parentheses.

| Incomplete | Complete |
|---|---|
| WHEN SET-35 ends, the application must remove the folders. | WHEN the cleanup interval ends, the application must remove each folder in `.onoo/tmp/` of a conversation that no chat view shows. The setting `pythonTmpCleanupMs` holds the interval (SET-35). |
| See [settings](06-settings.md) for the interval. | The setting `pythonTmpCleanupMs` holds the interval (SET-35). |

A specification holds no link to a different file, because a link breaks when
a file moves. The identifier names the page through the prefix table.

## One requirement for each behavior

One requirement states a behavior, in the specification of the module that
owns it. That requirement holds the trigger, the values, and the result.

```gherkin
Given a behavior that one requirement states
When a different page of docs/reference/ uses that behavior
Then that page names the behavior in words
And that page puts the identifier of the owner in parentheses
And that page holds no copy of the values of the owner
```

## Name the behavior

A requirement names the behavior and its result. It names no field, value of
a field, type, or name of the code. IF a user, the model, or a program
outside the application reads or writes a name, THEN the requirement may name
it: a key of the settings file, a path that the user sees, the name of a tool
that the model calls.

| Implementation | Behavior |
|---|---|
| The harness writes `used_tokens` on the line. | The line records the tokens that the request used. |
| `TranscriptService.flush()` runs every 5 s. | The application saves the transcript 5 s after the last change. |

A change of the code to match the words of a requirement starts only after
the requirement passes this test.

## Check each file

Run the check on each file that you wrote or changed:

```sh
<skill>/tools/ste/ste-check <file> --workspace <workspace>
```

- Repair each error that the tool reports.
- IF the tool rejects a word that names a thing of this project, THEN add
  the word to `<workspace>/docs/project-terms.txt`, one word on each line,
  with a comment that gives its meaning. STE rule 1.6 permits a technical
  name.
- IF the tool rejects a word of ordinary English, THEN use the approved word
  that the tool gives.

Run the check on an English file only.

## Flow

```lnl
START:
  DO    read docs/reference/README.md, the exemplar, and the specifications that own the behaviors the new text uses
  DO    write or change the requirements in the shape of the exemplar
CHECK_STE:
  ADD   1 to <s>
  STOP  show the errors of ste-check and ask the human how to continue IF <s> >= 4
  DO    run <skill>/tools/ste/ste-check on each file written, with --workspace <workspace>
  ASK   does ste-check report an error?
  JUMP  REVIEW IF no
  DO    repair each error, or add a technical name to docs/project-terms.txt
  JUMP  CHECK_STE
REVIEW:
  CHECK each requirement opens with an EARS trigger or states a rule that is always true, and holds one RFC 2119 obligation word
  CHECK each requirement names the behavior and its result, and a name of the code only when a user, the model, or an outside program uses it
  CHECK each requirement reads complete when its parentheses go away
  CHECK each behavior has one owner requirement; each other page names it and gives the identifier
  CHECK each new identifier takes the next free number; each removed one stays retired
  CHECK each new prefix is in the table of docs/reference/README.md
  CHECK ste-check reports 0 errors on each file written
REPLY:
  SAY   the files, the identifiers added or retired, and the result of ste-check
  END
```
