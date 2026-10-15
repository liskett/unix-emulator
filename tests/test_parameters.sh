#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 tests/build_vfs.py > /dev/null
python3 -m src.main --vfs tests/vfs/minimal.zip --script tests/start_ok.txt
echo "TEST PASSED"