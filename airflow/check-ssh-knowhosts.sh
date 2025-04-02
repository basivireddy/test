#!/bin/bash

# Check if the ~/.ssh directory exists
if [ -d "$HOME/.ssh" ]; then
    echo "SSH directory exists: $HOME/.ssh"
else
    echo "SSH directory does NOT exist!"
    exit 1
fi

# Check if the known_hosts file exists
if [ -f "$HOME/.ssh/known_hosts" ]; then
    echo "SSH known_hosts file exists: $HOME/.ssh/known_hosts"
else
    echo "SSH known_hosts file does NOT exist!"
    exit 2
fi
