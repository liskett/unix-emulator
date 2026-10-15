#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m src.main --script tests/start_ok.txt
echo "TEST PASSED"