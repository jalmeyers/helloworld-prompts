---
name: helloworld-prompts
description: A library of reusable prompts for learning, writing, meetings and planning. Use when the user asks what prompts are in the library, asks for prompts on a topic or category, or asks to run one of these prompts by name.
---

# Hello World Prompt Library

## How the library is organized

- `prompts/<category>/` holds the prompts, one Markdown file each. Each category folder has an
  `_index.md` that is **not** a prompt: it gives the category's `title`, a one-line `description`,
  an optional `weight` (lower comes first) and a longer explanation in its body.
- Each prompt file has front matter, then the prompt text as its body:
  - `title`, `description`: what the prompt is and does
  - `tags`: cross-cutting labels, explained in `tags/<tag>/_index.md`
  - `inputs`: the names of the `[PLACEHOLDERS]` the prompt needs
  - `weight` (optional): order within its category, lower first
- `tags/<tag>/_index.md` gives each tag's title, a one-line description and an explanation.

## When the user asks what prompts are available

List the categories in `weight` order, using each category's title and description. Under each,
list its prompts (in `weight` order) with their title and description. Keep it scannable.

## When the user asks for prompts on a topic, category or tag

Match the request to a category folder or a tag (by name, description or explanation). Say in one
line what that category or tag covers, then list the matching prompts.

## When the user asks to run a prompt

1. Find the prompt whose title or file name best matches the request.
2. Read the prompt body and its `inputs`.
3. If any input isn't already answered by the conversation, ask the user for all the missing ones
   in a single message. Use the input names as plain-language questions.
4. Follow the prompt, with the placeholders filled in, as if the user had typed it.
