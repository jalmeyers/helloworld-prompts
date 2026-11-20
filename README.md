# Hello World Prompt Library

A library of reusable prompts, packaged as a Claude skill. This repo holds only the content, and
every convention here exists to make the library useful **on its own**. A website, such as
`helloworld-prompts-site`, which includes this repo as a git submodule, is just one reader of it.

```
prompts/<category>/_index.md   ← what the category is for
prompts/<category>/<prompt>.md ← one file per prompt
tags/<tag>/_index.md           ← what each tag means
skill/SKILL.md                 ← tells Claude how to use all of the above
scripts/check.py               ← checks that everything follows the spec below
scripts/build-skill.sh         ← checks, then builds the skill folder and zip into dist/
.github/workflows/             ← runs the check on every push and PR; builds the zip for each release
```

## The spec

### Prompts: `prompts/<category>/<prompt-name>.md`

```markdown
---
title: "Say No Politely"
description: "Decline a request clearly and kindly, while keeping the relationship intact."
tags: ["email"]
inputs: ["WHAT I'M DECLINING", "WHO'S ASKING"]
weight: 3
---
Before you start, ask me for any values in square brackets that I haven't filled in. Ask for all of them in one message.

Help me write a short message declining [WHAT I'M DECLINING]. It's from [WHO'S ASKING].
…
```

| Field | Required | What it's for | Used by the skill | Used by the site |
|---|---|---|---|---|
| `title` | yes | The prompt's name. Must be unique across the library. | finding prompts by name | page title, cards |
| `description` | yes | One line saying what it does. | listing prompts | cards, search |
| `tags` | yes | Cross-cutting labels (can be `[]`). Lowercase, use-dashes. | finding prompts by topic | tag pages, search |
| `inputs` | yes | Every `[PLACEHOLDER]` in the prompt (can be `[]`). | knowing what to ask for | "You'll need" list |
| `weight` | no | Order within the category. Lower comes first. | ordering lists | ordering lists |
| `draft` | no | `true` while a prompt is being worked on. | left out of the skill | hidden from the site |

Rules:

- **One folder deep.** Every prompt lives in a category folder, e.g. `prompts/writing/`. No prompts at the top level, no sub-sub-folders.
- **Placeholders** are UPPERCASE in square brackets, like `[PASTE DRAFT]`. Each one must be listed in `inputs`, and each input must appear in the prompt.
- **Opening line.** Prompts with inputs start with: *"Before you start, ask me for any values in square brackets that I haven't filled in. Ask for all of them in one message."* This makes Claude ask for anything left unfilled, whether the prompt was copied from the site or run through the skill.
- **Value format.** Strings and lists are written as JSON (`"text"`, `["a", "b"]`), numbers and `true`/`false` bare, one field per line. Adding a new field means adding it here and to `scripts/check.py`.

### Categories: `prompts/<category>/_index.md`

```markdown
---
title: "Writing"
description: "Prompts that improve or draft things you'll send."
weight: 3
---
A longer explanation of the category.
```

`title` and `description` are required. `weight` orders the categories.

### Tags: `tags/<tag>/_index.md`

Same format as categories, without `weight`. Every tag used by a prompt needs one, and every tag
explained here must be used by at least one prompt.

## Check the library

```bash
python3 scripts/check.py
```

It lists every problem (missing fields, placeholders not in `inputs`, unexplained tags, duplicate
titles…) and fails if there are any. It runs automatically on every push and pull request, and
before every skill build. No dependencies beyond Python 3.

## Work on a draft

Add `draft: true` to the prompt. It stays out of the released skill and off the public site. To try it:

```bash
./scripts/build-skill.sh --drafts    # skill including drafts, for testing in Claude
```

On the site, `make serve-drafts` previews with drafts shown. Remove the `draft` line to publish.

## Release a new version

```bash
git tag v0.2.0
git push --tags
```

GitHub Actions builds `helloworld-prompts.zip` (without drafts) and attaches it to the release.
The site's download link always points to the latest release.

## Install the skill

- **Claude app:** download `helloworld-prompts.zip` from the latest release and upload it in Settings → Skills.
- **Claude Code:**
  ```bash
  ./scripts/build-skill.sh
  mkdir -p ~/.claude/skills && cp -r dist/helloworld-prompts ~/.claude/skills/
  ```
