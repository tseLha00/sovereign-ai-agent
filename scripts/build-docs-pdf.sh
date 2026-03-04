#!/usr/bin/env bash
set -euo pipefail

OUT="IPA_Documentation.pdf"

# Choose engine automatically
ENGINE="xelatex"
if ! command -v xelatex >/dev/null 2>&1; then
  if command -v wkhtmltopdf >/dev/null 2>&1; then
    ENGINE="wkhtmltopdf"
  else
    echo "❌ No PDF engine found."
    echo "Install one of:"
    echo "  - xelatex (recommended): MacTeX / MiKTeX / texlive-xetex"
    echo "  - wkhtmltopdf: brew install wkhtmltopdf"
    exit 1
  fi
fi

FILES=(
  "docs/00-index.md"
  "docs/A01-scope.md"
  "docs/A02-A03-research-log.md"
  "docs/A04-timeplan.md"
  "docs/A05-risk-log.md"
  "docs/A12-dod-test-concept.md"
  "docs/A13-operation-and-handover.md"
  "docs/H08-performance-monitoring.md"
  "docs/qa/perf-baselines.md"
  "docs/decisions/H01-runtime-decision.md"
)

# Add journals (sorted)
while IFS= read -r f; do FILES+=("$f"); done < <(ls -1 docs/journal/day-*.md 2>/dev/null | sort)

# Add meeting notes (sorted by filename/date)
while IFS= read -r f; do FILES+=("$f"); done < <(ls -1 evidence/meeting-notes/*.md 2>/dev/null | sort)

pandoc \
  "${FILES[@]}" \
  -o "$OUT" \
  --pdf-engine="$ENGINE" \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=11pt

echo "✅ Built: $OUT (engine=$ENGINE)"