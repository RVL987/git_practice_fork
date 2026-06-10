#!/bin/bash
# check_line_limits.sh

FAILED=0

while IFS= read -r file; do
  
  [[ "$file" == *"/.venv/"* ]] && continue
  [[ "$file" == *"/.git/"* ]] && continue

  
  LINES=$(wc -l < "$file" | xargs)
  
  if [ "$LINES" -gt 100 ]; then
    echo " ERROR: $file exceeds the 100-line limit ($LINES lines)."
    FAILED=1
  else
    echo " PASS: $file ($LINES lines)"
  fi
done < <(find . -type f -name "*.py")

if [ "$FAILED" -eq 1 ]; then
  exit 1
fi

echo "All Python files are within the 100-line limit."
exit 0
