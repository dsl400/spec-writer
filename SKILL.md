---
name: spec-writer
description: Use when the user asks to write, change, or review a specification (specificație) under docs/reference/. Writes each requirement in EARS with RFC 2119 obligation words, in ASD-STE100, and checks each file with the ste-check tool that comes with this skill.
user-invocable: true
---

# Spec Writer

A specification states what the application must do. It names the behavior
and its result. It does not name the code that does it.

`<skill>` is the folder of this file. `<workspace>` is the root of the project
that holds `docs/`.

## The shape of a file

A specification holds these parts, in this order:

1. **The title**: `# <NN> — <Subject>`. `<NN>` is the number of the file.
2. **The principle**: the idea of the specification, in prose. Add a code
   block that shows the shape when a shape exists.
3. **The requirements**: a list of requirement items.
4. **The verification**: the document, the trace, or the test that shows that
   the requirements hold.

WHEN the project has an exemplar file, the new file takes the shape of the
exemplar. The project names its exemplar in its rules.

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
- The project keeps a table of the prefixes in use. Add the prefix of a new
  specification to that table.

## A requirement is complete alone

A reader understands a requirement with no other page open. The requirement
names in words each thing it uses. WHEN the reader needs the definition of
such a thing, the sentence ends with the identifier of that definition in
parentheses.

```markdown
- **SHL-24** — WHEN the cleanup interval ends, the application must remove
  each folder in `.onoo/tmp/` of a conversation that no chat view shows. The
  setting `pythonTmpCleanupMs` holds the interval (SET-35).
```

The sentence is complete when you remove the parentheses. A specification
holds no link to a different file, because a link breaks when a file moves.

## One requirement for each behavior

One requirement states a behavior, in the specification of the module that
owns it. That requirement holds the trigger, the values, and the result. A
different specification names that behavior in words and puts the identifier
of the owner in parentheses. It does not copy the values.

## Behavior, not implementation

A requirement names the behavior and its result. It does not name a field, a
value of a field, a type, or a name of the code. IF a user, the model, or a
program outside the application reads or writes a name, THEN the requirement
may name it: a key of the settings file, a path that the user sees, the name
of a tool that the model calls.

## Check each file

Run the check on each file that you wrote or changed:

```sh
<skill>/tools/ste/ste-check <file> --workspace <workspace>
```

1. Repair each error that the tool reports.
2. IF the tool rejects a word that names a thing of this project, THEN add
   the word to `<workspace>/docs/project-terms.txt`, one word on each line,
   with a comment that gives its meaning. STE rule 1.6 permits a technical
   name.
3. IF the tool rejects a word of ordinary English, THEN use the approved word
   that the tool gives.
4. Run the check again until it reports 0 errors.

Run the check on an English file only.

## Procedure

1. Read the exemplar and the prefix table of the project.
2. Read the specifications that own the behaviors that the new text uses.
3. Write or change the requirements.
4. Run the check on each file and repair it.
5. Report the files, the identifiers that you added or retired, and the
   result of the check.
