# Hello World Prompt Library

A library of reusable prompts, packaged as a Claude skill. This repo holds only the content.
The website that displays it lives in a separate repo (`helloworld-prompts-site`), which pulls
this one in as a git submodule.

```
prompts/                  ← one .md file per prompt
tags/<tag>/_index.md      ← optional explanation for each tag
skill/SKILL.md            ← tells Claude how to use prompts/ and tags/
scripts/build-skill.sh    ← builds the skill folder and zip into dist/
.github/workflows/        ← builds the zip and attaches it to each GitHub Release
```

## Add a prompt

Create `prompts/my-new-prompt.md`:

```markdown
---
title: "My New Prompt"
description: "One line saying what it does. Shows on the site and in Claude's list."
tags: ["sales", "email"]
---
Before you start, ask me for any values in [SQUARE BRACKETS] that I haven't filled in. Ask for all of them in one message.

The prompt text goes here. Use [SQUARE BRACKETS] for anything the user fills in.
```

Keep the first line in every prompt. It makes Claude ask for any placeholders the user forgot
to fill in, whether the prompt was copied from the site or run through the skill.

## Add or explain a tag

Any tag used in a prompt works on its own. To give it an explanation, create
`tags/<tag>/_index.md`:

```markdown
---
title: "Sales"
description: "One line shown on the site's tag overview and in Claude's tag listing."
---
A longer explanation shown at the top of the tag's page.
```

## Release a new version

```bash
git tag v0.2.0
git push --tags
```

GitHub Actions builds `helloworld-prompts.zip` and attaches it to the release. The site's
"Download" link always points to the latest release, so people get the new zip right away.

To see the site pick up new prompts, update the submodule in the site repo (see its README).

## Install the skill

- **Claude app:** download `helloworld-prompts.zip` from the latest release and upload it in Settings → Skills.
- **Claude Code:**
  ```bash
  ./scripts/build-skill.sh
  mkdir -p ~/.claude/skills && cp -r dist/helloworld-prompts ~/.claude/skills/
  ```
