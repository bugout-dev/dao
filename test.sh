#!/usr/bin/env sh

# Expects a Python environment to be active in which `dao` has been installed for development.
# You can set up the local copy of `dao` for development using:
# pip install -e .[dev]

usage() {
    echo "Usage: $0"
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]
then
    usage
    exit 2
fi

TEST_COMMAND=${@:-discover}

brownie compile
set -x
python -m unittest $TEST_COMMAND
