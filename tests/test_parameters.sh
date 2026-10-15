#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m src.main --vfs my_vfs --script tests/start_ok.txt
echo "TEST PASSED"