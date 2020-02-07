#!/bin/bash

# Exit on error
set -e

# Trace commands as we run them:
set -x

# Print error message and exit with error code 1
function die {
    echo "$1"
    exit 1
}

# Check the number of arguments
[ $# -ge 3 ] || die "usage: $0 <playbook> <inventory> <vault-password-file>"

PLAYBOOK=$1
INVENTORY=$2
VAULT_PASSWORD_FILE=$3

ansible-playbook $PLAYBOOK -i $INVENTORY --vault-password-file $VAULT_PASSWORD_FILE
