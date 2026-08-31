#!/usr/bin/env bash
# Human-in-the-loop (HITL) reproduction loop template.
# Use when a bug requires manual browser interaction, UI clicks, or interactive terminal auth.
# The agent drives the script, prompting the human operator for specific actions and observations.
#
# Usage:
#   bash hitl-loop.template.sh
#
# Helpers:
#   step "<instruction>"          → Displays instruction, pauses for Enter
#   capture VAR "<question>"      → Prompts question, records response into variable
#
# At the end, captured values are emitted as structured KEY=VALUE pairs for parsing.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Press Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- Customize Steps Below ----------------------------------------------------

step "Open the application at http://localhost:3000 and log in."

step "Navigate to the target dashboard or triggering view."

capture ERRORED "Perform the action (e.g. click 'Export'). Did an error occur? (y/n)"

capture ERROR_MSG "Paste the full error message or HTTP status code (or 'none'):"

capture CONSOLE_LOGS "Paste any console or network errors from DevTools (or 'none'):"

# --- End Customization --------------------------------------------------------

printf '\n--- Captured Diagnosis Evidence ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
printf 'CONSOLE_LOGS=%s\n' "$CONSOLE_LOGS"
