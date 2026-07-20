#!/usr/bin/env bash
# macOS/Linux counterpart of update.ps1: pull the latest skill updates.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${1:-$(cd "$SCRIPT_DIR/.." && pwd)}"

git -C "$REPO_ROOT" pull --ff-only
