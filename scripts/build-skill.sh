#!/usr/bin/env bash
# Packages the library as a Claude skill.
#   dist/helloworld-prompts/       -> copy this folder into ~/.claude/skills/ (Claude Code)
#   dist/helloworld-prompts.zip    -> upload this in the Claude app
# The GitHub release workflow runs this script and attaches the zip to each release.
set -euo pipefail
cd "$(dirname "$0")/.."

NAME=helloworld-prompts
OUT="dist/$NAME"

rm -rf dist && mkdir -p "$OUT"
cp skill/SKILL.md "$OUT/"
cp -r prompts tags "$OUT/"

# Use zip if installed; otherwise fall back to Python.
if command -v zip >/dev/null; then
  (cd dist && zip -qr "$NAME.zip" "$NAME")
else
  (cd dist && python3 -m zipfile -c "$NAME.zip" "$NAME")
fi

echo "Skill folder: $OUT"
echo "Skill zip:    dist/$NAME.zip"
