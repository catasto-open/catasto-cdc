#!/bin/bash
set -e

echo "Running mypy..."
mypy cdc

echo "Running bandit..."
bandit -c pyproject.toml -r cdc
