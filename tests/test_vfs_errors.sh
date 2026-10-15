#!/usr/bin/env bash
cd "$(dirname "$0")/.."
python3 tests/build_vfs.py > /dev/null
fail=0

echo "Test 1: missing VFS"
python3 -m src.main --vfs tests/vfs/missing.zip --script tests/stage3_minimal.txt && fail=1

echo "Test 2: not a zip"
python3 -m src.main --vfs tests/vfs/minimal/hello.txt --script tests/stage3_minimal.txt && fail=1

if [ "$fail" -eq 0 ]; then
    echo "ALL ERROR TESTS PASSED"
    exit 0
else
    echo "TEST FAILED"
    exit 1
fi