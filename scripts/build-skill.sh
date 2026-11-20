#!/usr/bin/env bash
# Packages the library as a Claude skill.
#   ./scripts/build-skill.sh            -> published prompts only (drafts left out)
#   ./scripts/build-skill.sh --drafts   -> include drafts, for testing them in Claude
#
# Output:
#   dist/helloworld-prompts/       -> copy this folder into ~/.claude/skills/ (Claude Code)
#   dist/helloworld-prompts.zip    -> upload this in the Claude app
# The GitHub release workflow runs this script and attaches the zip to each release.
set -euo pipefail
cd "$(dirname "$0")/.."

NAME=helloworld-prompts
OUT="dist/$NAME"
INCLUDE_DRAFTS=false
[[ "${1:-}" == "--drafts" ]] && INCLUDE_DRAFTS=true

# Refuse to build a broken library.
python3 scripts/check.py

rm -rf dist && mkdir -p "$OUT"
cp skill/SKILL.md "$OUT/"
cp -r tags "$OUT/"

# Copy prompts/, keeping the folders, and skipping drafts unless asked.
# A draft has "draft: true" between the opening and closing --- lines.
is_draft() { awk '/^---$/{n++; next} n==1 && /^draft:[[:space:]]*true[[:space:]]*$/{found=1} END{exit !found}' "$1"; }
skipped=0
while IFS= read -r -d '' f; do
  if ! $INCLUDE_DRAFTS && is_draft "$f"; then
    skipped=$((skipped + 1)); continue
  fi
  mkdir -p "$OUT/$(dirname "$f")"
  cp "$f" "$OUT/$f"
done < <(find prompts -name '*.md' -print0)

# Use zip if installed; otherwise fall back to Python.
if command -v zip >/dev/null; then
  (cd dist && zip -qr "$NAME.zip" "$NAME")
else
  (cd dist && python3 -m zipfile -c "$NAME.zip" "$NAME")
fi

echo "Skill folder: $OUT"
echo "Skill zip:    dist/$NAME.zip"
$INCLUDE_DRAFTS && echo "Drafts:       included" || echo "Drafts:       $skipped left out (use --drafts to include)"
