#!/bin/bash
set -e

echo "Running mypy..."
mypy catasto-cdc

echo "Running bandit..."
bandit -c pyproject.toml -r catasto-cdc
