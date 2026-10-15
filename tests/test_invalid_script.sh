#!/usr/bin/env bash
cd "$(dirname "$0")/.."
if python3 -m src.main --script tests/missing.txt; then
    echo "TEST FAILED"
    exit 1
else
    echo "TEST PASSED"
fi