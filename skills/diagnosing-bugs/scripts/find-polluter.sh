#!/usr/bin/env bash
# Bisection script to find which test pollutes shared state or creates unwanted artifacts.
# Usage: ./find-polluter.sh <file_or_dir_to_check> <test_pattern> [test_command]
# Example: ./find-polluter.sh '.git' 'src/**/*.test.ts' 'npm test --'

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <file_or_dir_to_check> <test_pattern> [test_command]"
  echo "Example: $0 '.git' 'src/**/*.test.ts' 'npm test --'"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="$2"
TEST_COMMAND="${3:-npm test --}"

echo "🔍 Searching for test causing pollution: $POLLUTION_CHECK"
echo "Test pattern: $TEST_PATTERN"
echo "Test command: $TEST_COMMAND"
echo ""

TEST_FILES=$(find . -path "$TEST_PATTERN" | sort)
TOTAL=$(echo "$TEST_FILES" | grep -v '^$' | wc -l | tr -d ' ')

if [ "$TOTAL" -eq 0 ]; then
  echo "❌ No test files matched pattern: $TEST_PATTERN"
  exit 1
fi

echo "Found $TOTAL test files to evaluate."
echo ""

COUNT=0
for TEST_FILE in $TEST_FILES; do
  COUNT=$((COUNT + 1))

  # Pre-check for existing pollution
  if [ -e "$POLLUTION_CHECK" ]; then
    echo "⚠️  Pollution artifact already exists before test $COUNT/$TOTAL ($TEST_FILE)"
    echo "   Aborting bisection. Clean up '$POLLUTION_CHECK' before rerunning."
    exit 1
  fi

  echo "[$COUNT/$TOTAL] Testing: $TEST_FILE"

  # Run test
  $TEST_COMMAND "$TEST_FILE" > /dev/null 2>&1 || true

  # Check if pollution appeared
  if [ -e "$POLLUTION_CHECK" ]; then
    echo ""
    echo "🎯 FOUND POLLUTER TEST!"
    echo "   Test file: $TEST_FILE"
    echo "   Created artifact: $POLLUTION_CHECK"
    echo ""
    echo "Artifact details:"
    ls -la "$POLLUTION_CHECK"
    echo ""
    echo "To investigate individually:"
    echo "  $TEST_COMMAND $TEST_FILE"
    exit 1
  fi
done

echo ""
echo "✅ No polluter found - all test executions ran clean."
exit 0
