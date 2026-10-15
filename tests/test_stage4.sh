#!/usr/bin/env bash
cd "$(dirname "$0")/.."
python3 tests/build_vfs.py > /dev/null

echo "Success case..."
python3 -m src.main --vfs tests/vfs/multiple.zip --script tests/stage4_success.txt || exit 1

echo "Error case..."
python3 -m src.main --vfs tests/vfs/multiple.zip --script tests/stage4_errors.txt

echo "STAGE 4 TESTS PASSED"