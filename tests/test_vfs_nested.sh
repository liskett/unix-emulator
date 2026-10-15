#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 tests/build_vfs.py > /dev/null
python3 -m src.main --vfs tests/vfs/nested.zip --script tests/stage3_nested.txt
echo "TEST PASSED"