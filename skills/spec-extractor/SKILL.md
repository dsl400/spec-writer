---
name: spec-extractor
description: Use when the user asks to extract or update the functional specs (specificații funcționale) of a screen, dialog, or dashboard from the existing app into docs/specs/, and to file the application gaps found on the way as GitHub issues.
user-invocable: true
metadata:
  source: https://github.com/dsl400/spec-writer
  version: 0.1.0
---

# Spec Extractor

Read the code to learn what the application does today. Write that behavior
as a user or an auditor sees it: screens, fields, buttons, messages, rules,
and roles.

A spec states what the code does today, as a fact. When the UI and the server
operate differently, the spec states the two behaviors, each with its actor.

| Judgment | Fact |
|---|---|
| The dialog wrongly limits the special characters. | The dialog accepts `! @ # $ % ^ & *`. The server accepts all special characters. |
| The user should be able to edit a role. | (a spec line for what exists; the gap goes to the gaps file) |

`<workspace>` is the root of the project that holds `docs/`.

## Input

A screen, route, or area (`settings/users`, `dashboard`). With no input,
compare `docs/specs/` against the routes and propose the next screen that has
no spec.

## Hierarchy

The tree follows the screens a user navigates: one folder for each screen
segment. The file with the name of its folder holds the general spec; child
screens and dialogs sit next to it.

```
docs/specs/
  dashboard/dashboard.md          general dashboard behavior
  dashboard/<dashboard-name>.md   one dashboard
  settings/settings.md            settings layout, tabs, navigation
  settings/users/users.md         the Users screen
  settings/users/add-user.md      the Add New User dialog
```

- File and folder names are kebab-case, from the screen name or the dialog action.
- A dialog or drawer gets its own file next to the screen that opens it.
- Content that all children share lives in the parent file. Children link to it.

## Where to learn the behavior

- The route definitions give the screens.
- The templates give the exact labels, buttons, and messages. Copy them word
  for word into a code span (`Add New User`), so the screen and the spec match.
- The component code, the server handler, and the database procedure give the
  rules, validations, errors, and permissions.

The spec holds the result of this research, in the words of a user.

## File template

```markdown
# `Add New User`

Parent: [Users](users.md)

## Purpose
The `Add New User` dialog lets an administrator create an account for a new user.

## Content
- The dialog shows the fields `Full Name`, `Email`, `Password` and `Role`.
- The dialog shows the buttons `Cancel` and `Create User`.

## Actions
### Create a user
1. Type the full name in `Full Name`.
2. Select `Create User`.
3. The system shows the message `User "{name}" created successfully`.

## Rules
- R1. All four fields are mandatory.
- R2. The email address must not be the address of a different user (see [Users](users.md) R6).

## Errors
The dialog shows a validation message in a box above the fields.

- If the full name has less than 2 characters, the message is `Name must be at least 2 characters long`.

## Permissions
- Only a user with the `Administrator` role can create a user.
```

- The title is the label of the screen or dialog, in a code span.
- Each fact is a sentence in a list: "`Email` is a text field with the example
  text `john@example.com`."
- `{name}` in a message marks a value that the system puts in the text.
- One sentence before the error messages says where the message shows.
- Keep the sections that have content, in the order of the template.
- The steps of a user take the imperative ("Select `Save`."); the behavior of
  the system takes the present tense.
- The condition comes first: "If the email exists, the system shows …".
- "Select" is a click or a key; "remove" is a delete.
- One term for each concept: the term on the UI label, the same in all files.

## Rule numbers

Tests and issues name a rule by its number, so a number stays with its rule.

- A new rule gets the next free number of the file.
- A rule keeps its number when its text changes.
- A link to a rule of a different file has the link and the number:
  `[Users](users.md) R7`.

## Gaps

When the research shows a defect or a missing function, the spec states what
the code does and the gap goes to
`<workspace>/reports/application-gaps/<module>-gaps.md`. `<module>` is the
top folder under `docs/specs/`.

| Category | When | Labels |
|---|---|---|
| `broken` | The code does not do what the screen offers: a button with no handler, an error that never shows, a field the server ignores | `type:bug` `class:minor-bug`, or `class:major-bug` when it blocks a core flow or corrupts data |
| `mismatch` | The UI and the server apply different rules to the same input | `type:bug` `class:minor-bug` |
| `missing` | A function a user of this screen needs is absent | `type:feature` `class:feature` |
| `ux` | A wrong label, a typo, a message that does not tell the user what to do | `type:bug` `class:aesthetic` |

```markdown
# <Module> gaps

## G1. Server accepts an email the dialog rejects
- Category: mismatch
- Screen: [Add New User](../../docs/specs/settings/users/add-user.md) R2
- Evidence: `ui/src/app/features/settings/users/add-user.component.ts:48`, `server/api/users/create.go:31`
- Facts: The dialog rejects `a@b`. `POST /api/v1/users` accepts it.
- Issue: —
```

- Add each gap the moment you find it. The code stays as it is.
- A gap keeps its `G` number. A new gap gets the next free number of the file.
- A gap that is already in the file gets a new `Screen` or `Evidence` line.
- A gap that the code no longer has gets `Status: closed`; the entry stays.

## File the gaps

One GitHub issue holds the open gaps of one category in one module. The
repository is the `origin` of the workspace (`gh repo view --json nameWithOwner`).

- Title: `[<Module>] <Category> gaps: <short scope>`.
- Body: one checklist item for each gap, `- [ ] G<n>. <title>`, then its
  `Screen`, `Evidence`, and `Facts` lines, indented.
- Labels: `mod:<module>`, the labels of the category, `status:untested`,
  `test:none`. A `broken` issue takes the highest class of its gaps.
- An open issue for the same module and category gets the new gaps as a
  comment (`gh issue comment`).

## Check each file

Check each spec with the check of the `spec-writer` skill, which comes in
the same package. That skill holds ste-check and the steps to repair its
errors.

## Flow

```lnl
START:
  ASK   does the message approve the issues that an earlier turn showed?
  JUMP  FILE IF yes
  DO    read the routes, templates, component code, and server handlers of the screen
  DO    write the parent file when it is absent, then one file for each screen and each dialog
  DO    add each gap to reports/application-gaps/<module>-gaps.md the moment you find it
CHECK_STE:
  ADD   1 to <s>
  STOP  show the errors of ste-check and ask the human how to continue IF <s> >= 4
  DO    run the check of the spec-writer skill on each file written
  ASK   does the check report an error?
  JUMP  LABELS IF no
  DO    repair each error, or add a technical name to docs/project-terms.txt
  JUMP  CHECK_STE
LABELS:
  DO    search the UI source for each label and message in a code span, and correct each one the search does not find
  DO    open each relative link and repair each one that goes to no file
  ASK   is a gap open with Issue: — ?
  JUMP  REVIEW IF no
  STOP  show the groups of gaps, the title of each issue, and its G numbers, and ask the human to approve the issues IF yes
FILE:
  DO    create or comment each issue and write its number in the Issue line of each gap
  JUMP  REVIEW
REVIEW:
  CHECK each spec states what the code does today, with the actor of each behavior
  CHECK each label and message in a code span is found in the UI source
  CHECK each rule keeps its number, and each new rule takes the next free number
  CHECK each gap has a category, evidence with file:line, and facts
  CHECK the check of the spec-writer skill reports 0 errors on each file written
REPLY:
  SAY   the files written, the new gaps of each category, and each issue with its number and URL
  END
```
