#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
echo "Проверка: ошибки в скрипте пропускаются, выполнение продолжается"
python3 -m src.main --script tests/start_error.txt
echo "TEST PASSED"