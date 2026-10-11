#!/usr/bin/env bash

readonly INSTANCE_FILE=../state/instance.txt
readonly INSTANCE_NAME=$(cat "$INSTANCE_FILE")
OS=$(grep "^PRETTY_NAME=" /etc/os-release | cut -d'"' -f2)

# info

echo ""
echo "Instance: $INSTANCE_NAME"
echo "Running at: $OS"
echo ""