#!/bin/bash

echo "Running pyup_dirs..."
pyup_dirs --py38-plus --recursive catasto-cdc tests

echo "Running ruff..."
ruff catasto-cdc tests --fix

echo "Running black..."
black catasto-cdc tests
