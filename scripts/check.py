#!/usr/bin/env python3
"""Check that the library follows the spec in README.md.

Run from anywhere:  python3 scripts/check.py
Exits non-zero and lists every problem if anything is wrong. No dependencies.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
TAGS = ROOT / "tags"

OPENING_LINE = "ask me for any values in square brackets"
PLACEHOLDER = re.compile(r"\[([A-Z][A-Z0-9 '’/&-]*)\]")

PROMPT_FIELDS = {  # field: (type, required)
    "title": (str, True),
    "description": (str, True),
    "tags": (list, True),
    "inputs": (list, True),
    "weight": (int, False),
    "draft": (bool, False),
}
INDEX_FIELDS = {
    "title": (str, True),
    "description": (str, True),
    "weight": (int, False),
}

problems = []


def problem(path, msg):
    problems.append(f"{path.relative_to(ROOT)}: {msg}")


def parse(path):
    """Split a file into (front matter dict, body). Values follow the README rules:
    strings and lists are written as JSON ("text", ["a", "b"]); numbers and true/false bare."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        problem(path, "must start with --- front matter")
        return {}, text
    try:
        head, body = text[4:].split("\n---\n", 1)
    except ValueError:
        problem(path, "front matter is not closed with ---")
        return {}, text
    meta = {}
    for n, line in enumerate(head.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, raw = line.partition(":")
        if not sep:
            problem(path, f"line {n}: expected 'key: value'")
            continue
        key, raw = key.strip(), raw.strip()
        if raw in ("true", "false"):
            meta[key] = raw == "true"
        elif re.fullmatch(r"-?\d+", raw):
            meta[key] = int(raw)
        else:
            try:
                meta[key] = json.loads(raw)
            except json.JSONDecodeError:
                problem(path, f"line {n}: {key} must be a quoted string, a [\"list\"], a number or true/false")
    return meta, body


def check_fields(path, meta, spec):
    for field, (typ, required) in spec.items():
        if field not in meta:
            if required:
                problem(path, f"missing required field '{field}'")
            continue
        value = meta[field]
        if typ is int and isinstance(value, bool) or not isinstance(value, typ):
            problem(path, f"'{field}' must be a {typ.__name__}")
        elif typ is str and not value.strip():
            problem(path, f"'{field}' is empty")
        elif typ is list and not all(isinstance(v, str) and v for v in value):
            problem(path, f"'{field}' must be a list of non-empty strings")
    for field in meta.keys() - spec.keys():
        problem(path, f"unknown field '{field}' (add it to the spec in README.md first)")


def main():
    titles = {}
    used_tags = set()

    # Sections: every folder in prompts/ needs an _index.md
    for folder in sorted(p for p in PROMPTS.iterdir() if p.is_dir()):
        index = folder / "_index.md"
        if not index.exists():
            problem(folder, "folder needs an _index.md with a title and description")
        else:
            meta, _ = parse(index)
            check_fields(index, meta, INDEX_FIELDS)

    # Prompts
    for path in sorted(PROMPTS.rglob("*.md")):
        if path.name == "_index.md":
            continue
        depth = len(path.relative_to(PROMPTS).parts)
        if depth != 2:
            problem(path, "prompts must live exactly one folder deep, e.g. prompts/writing/my-prompt.md")
        meta, body = parse(path)
        check_fields(path, meta, PROMPT_FIELDS)

        title = meta.get("title")
        if isinstance(title, str):
            key = title.strip().lower()
            if key in titles:
                problem(path, f"title '{title}' is also used by {titles[key]}")
            titles[key] = path.relative_to(ROOT)

        for tag in meta.get("tags") or []:
            if tag != tag.lower() or " " in tag:
                problem(path, f"tag '{tag}' must be lowercase with no spaces (use-dashes)")
            used_tags.add(tag)

        found = set(PLACEHOLDER.findall(body))
        declared = set(meta.get("inputs") or [])
        for name in sorted(found - declared):
            problem(path, f"placeholder [{name}] is in the prompt but not listed in 'inputs'")
        for name in sorted(declared - found):
            problem(path, f"input '{name}' is listed in 'inputs' but [{name}] isn't in the prompt")
        if declared and OPENING_LINE not in body.lower():
            problem(path, "prompts with inputs must include the standard opening line (see README.md)")
        if not body.strip():
            problem(path, "prompt text is empty")

    # Tags: every tag used needs an explanation, and every explanation should be used
    for tag in sorted(used_tags):
        index = TAGS / tag / "_index.md"
        if not index.exists():
            problems.append(f"tags/{tag}/_index.md: missing (tag '{tag}' is used by a prompt)")
        else:
            meta, _ = parse(index)
            check_fields(index, meta, INDEX_FIELDS)
    for folder in sorted(p for p in TAGS.iterdir() if p.is_dir()):
        if folder.name not in used_tags:
            problem(folder, "tag has an explanation but no prompt uses it")

    if problems:
        print(f"✗ {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"✓ Library OK: {len(titles)} prompts, {len(used_tags)} tags")


if __name__ == "__main__":
    main()
