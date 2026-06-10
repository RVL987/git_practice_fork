#!/bin/bash
# run_pycodestyle.sh

# Ensure necessary environment variables are set
if [ -z "$GITHUB_TOKEN" ] || [ -z "$PR_NUMBER" ] || [ -z "$REPO" ]; then
  echo "Missing environment configuration. Ensure GITHUB_TOKEN, PR_NUMBER, and REPO are set."
  exit 1
fi

# Run pycodestyle and save output to a temporary file
pycodestyle . > lint_output.txt || true

if [ -s lint_output.txt ]; then
  echo "PEP 8 violations found. Preparing GitHub comment..."

  # Format output text as a markdown code block
  COMMENT_BODY=$(cat <<EOF
### ⚠️ PEP 8 Style Violations Detected
\`\`\`text
$(head -n 30 lint_output.txt)
\`\`\`
EOF
)

  # Append truncation message if output is long
  if [ $(wc -l < lint_output.txt) -gt 30 ]; then
    COMMENT_BODY="$COMMENT_BODY"$'\n'
  fi

  # Build a safe JSON payload using jq
  JSON_PAYLOAD=$(jq -n --arg body "$COMMENT_BODY" '{body: $body}')

  # Dispatch the payload using curl
  curl -s -X POST \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$REPO/issues/$PR_NUMBER/comments" \
    -d "$JSON_PAYLOAD"

  echo "Violations reported to PR."
  exit 1
else
  echo "No PEP 8 violations detected."
  exit 0
fi
