#!/bin/bash

# Check if the ~/.ssh directory exists
if [ -d "$HOME/.ssh" ]; then
    echo "SSH directory exists: $HOME/.ssh"
elif [ -f "$HOME/.ssh/known_hosts" ]; then
    echo "SSH known_hosts file exists: $HOME/.ssh/known_hosts"
else
    echo "create"
fi

