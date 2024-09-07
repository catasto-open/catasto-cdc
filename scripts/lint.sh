#!/bin/bash

echo "Running pyup_dirs..."
pyup_dirs --py310-plus --recursive cdc tests

echo "Running ruff..."
ruff cdc tests --fix

echo "Running black..."
black cdc tests
