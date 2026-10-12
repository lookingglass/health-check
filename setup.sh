#!/usr/bin/env bash
# health-check setup

set -euo pipefail

# vars
readonly boot_id_file="./state/boot_id"
readonly instance_id_file="./state/instance.txt"

# setup
mkdir -p state

# boot_id

if [[ ! -e "$boot_id_file" ]]; then
    cat "/proc/sys/kernel/random/boot_id" > "$boot_id_file" # boot_id for restart detection
    echo "created boot id file with current ID"
fi


# instance_id

if [[ ! -e "$instance_id_file" ]]; then
    ./utils/name_generator.py > "$instance_id_file" # random name, can be edited in ./state/instance.txt
    echo "created instance name"
fi