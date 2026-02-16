#!/usr/bin/env bash
set -e

# Simple installer for repository files and Python dependencies.
# to run: "bash install.sh"

PYTHON_BIN="${PYTHON_BIN:-python3}"
REPO_URL="https://github.com/JakeBodish/team_5_laser_tag.git"
TARGET_DIR="${TARGET_DIR:-team_5_laser_tag}"

# Install git first.
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y git
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y git
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y git
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -Sy --noconfirm git
elif command -v zypper >/dev/null 2>&1; then
  sudo zypper install -y git
elif command -v apk >/dev/null 2>&1; then
  sudo apk add git
elif command -v brew >/dev/null 2>&1; then
  brew install git
fi

if [[ -n "$REPO_URL" ]]; then
  echo "Cloning repository into $TARGET_DIR..."
  git clone "$REPO_URL" "$TARGET_DIR"
  REPO_DIR="$TARGET_DIR"
else
  REPO_DIR="$(pwd)"
  echo "Using current directory as repository: $REPO_DIR"
fi

echo "Using Python interpreter: $PYTHON_BIN"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install pygame

# socket, sqlite3, and queue are standard-library modules.
# add more when necessary
"$PYTHON_BIN" - <<'PY'
import socket
import sqlite3
import queue
print('Standard library modules available: socket, sqlite3, queue')
PY

echo "Done. Repository files available at: $REPO_DIR"

