#!/bin/bash

# Define a safe_tput function that only uses tput if it's available and working
safe_tput() {
  if command -v tput >/dev/null 2>&1; then
    tput "$@" 2>/dev/null || echo ""
  else
    echo ""
  fi
}

# Set color variables using safe_tput
RED=$(safe_tput setaf 1)
GREEN=$(safe_tput setaf 2)
YELLOW=$(safe_tput setaf 3)
BLUE=$(safe_tput setaf 4)
BOLD=$(safe_tput bold)
NC=$(safe_tput sgr0)  # No Color / Reset
