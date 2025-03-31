#!/bin/bash

# Set your S3 bucket and folder
BUCKET_NAME="your-bucket-name"
FOLDER_PREFIX="your-folder-name/"  # Ensure it ends with a slash
# Store current date in a variable
CURRENT_DATE=$(date +%Y%m%d)

# Print the date
echo "Today's date: $CURRENT_DATE"

# List all files in the S3 folder
FILES=$(aws s3 ls "s3://$BUCKET_NAME/$FOLDER_PREFIX" --recursive | awk '{print $4}')

declare -A files_dict

# Check if any files were found
if [ -z "$FILES" ]; then
    echo "No files found in S3 folder: s3://$BUCKET_NAME/$FOLDER_PREFIX"
    #files_dict["data"]="not exist"
    #return my_dict
    #exit 1
fi

# Loop through each file and count lines
for FILE in $FILES; do
    echo "Processing: $FILE"
    LINE_COUNT=$(aws s3 cp "s3://$BUCKET_NAME/$FILE" - | wc -l)
    echo "File: $FILE, Lines: $LINE_COUNT"
    # Insert key-value pairs
    files_dict[$FILE]= $LINE_COUNT
done

LOCAL_DIR="/tmp/s3_files"
SFTP_HOST="sftp.example.com"
SFTP_USER="your_sftp_username"
SSH_KEY="~/.ssh/id_rsa"  # Path to SSH private key
SFTP_DEST_DIR="/remote/sftp/path/"  # Target directory on SFTP
# Ensure local directory exists
mkdir -p "$LOCAL_DIR"


#ssh-keyscan -H $SFTP_HOST >> ~/.ssh/known_hosts 2>/dev/null

# Define SFTP host
SFTP_HOST="sftp.example.com"

# Known hosts file
KNOWN_HOSTS_FILE="$HOME/.ssh/known_hosts"

# Check if the host is already in known_hosts
if ssh-keygen -F "$SFTP_HOST" > /dev/null; then
    echo "✅ Host $SFTP_HOST is already in known_hosts."
else
    echo "⚠️  Host $SFTP_HOST not found in known_hosts. Adding now..."
    ssh-keyscan -H "$SFTP_HOST" >> "$KNOWN_HOSTS_FILE"
    echo "✅ Host $SFTP_HOST has been added to known_hosts."
fi


# Loop through dictionary keys & values
echo "list files and count"
for key in "${!files_dict[@]}"; do
    echo "$key: ${files_dict[$key]}"
    # "Downloading files from S3..."
    if [[ "${files_dict[$key]}" -gt "20000" ]]; then
       aws s3 cp "s3://$BUCKET_NAME/$key" "$LOCAL_DIR/"
    fi
    
done



echo "Transferring files to SFTP..."
for LOCAL_FILE in "$LOCAL_DIR"/*; do
    if [ -f "$LOCAL_FILE" ]; then
        echo "Uploading $LOCAL_FILE to SFTP..."
        scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "$SSH_KEY" "$LOCAL_FILE" "$SFTP_USER@$SFTP_HOST:$SFTP_DEST_DIR"
    fi
done

# Cleanup local directory
rm -rf "$LOCAL_DIR"
echo "Transfer completed!"

return files_dict
