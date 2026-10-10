#!/bin/bash

######################

# Show line numbers in trace mode
export PS4='+$LINENO: '

# Enable trace mode
set -x

# Enable strict mode
set -e
set -u
set -o pipefail

# using trap on error
trap 'echo "Error occurred at line $LINENO"; exit 1' ERR

######################

echo "Running..."

false  # Causes an error

echo "This line won't be executed."