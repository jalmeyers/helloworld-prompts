---
name: helloworld-prompts
description: A small library of reusable prompts (Hello World, Explain Like I'm New, Meeting Notes to Follow-up Email). Use when the user asks what prompts are in the library, asks for prompts on a topic or tag, or asks to run one of these prompts by name.
---

# Hello World Prompt Library

The prompts live in the `prompts/` folder next to this file, one Markdown file per prompt.
Each file has frontmatter (`title`, `description`, `tags`) and the prompt text as its body.
Placeholders are written in `[SQUARE BRACKETS]`.

The `tags/` folder has one folder per tag. Its `_index.md` gives the tag's title, a one-line
`description`, and a longer explanation in the body.

## When the user asks what prompts are available

Read the frontmatter of every file in `prompts/` and list each prompt's title and description.
If there are more than a handful, group them by tag, using the tag titles from `tags/`.

## When the user asks for prompts on a topic or tag

Match the request to a tag in `tags/` (by name, description or explanation). Briefly say what
the tag covers, then list the prompts that carry it.

## When the user asks to run a prompt

1. Find the file whose title or file name best matches what the user asked for.
2. Read the prompt body.
3. If any `[PLACEHOLDER]` isn't already answered by the conversation, ask the user for it. Ask for all missing ones in a single message.
4. Follow the prompt, with the placeholders filled in, as if the user had typed it.
