#!/bin/bash

# Set terminal colors using tput if available
if command -v tput >/dev/null 2>&1; then
  RED=$(tput setaf 1)
  GREEN=$(tput setaf 2)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  BOLD=$(tput bold)
  NC=$(tput sgr0) # No Color / Reset
else
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  BOLD=""
  NC=""
fi

# Sample usage
echo "${GREEN}${BOLD}✓ Success:${NC} Everything is configured correctly!"
echo "${RED}${BOLD}✗ Error:${NC} Something went wrong!"
echo "${YELLOW}${BOLD}! Warning:${NC} Be cautious with this step."
echo "${BLUE}${BOLD}ℹ Info:${NC} Running the Seam Carver application."
