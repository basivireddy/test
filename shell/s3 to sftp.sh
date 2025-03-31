#!/bin/bash

# Set S3 bucket and SFTP details
S3_BUCKET="your-bucket-name"
S3_PREFIX="your-folder-name/"  # Prefix inside S3 bucket
LOCAL_DIR="/tmp/s3_files"       # Temporary local folder
SFTP_HOST="sftp.example.com"
SFTP_USER="your_sftp_username"
SFTP_PASSWORD="your_sftp_password"  # Use SSH key instead for better security
SFTP_DEST_DIR="/remote/sftp/path/"  # Target directory on SFTP

# Ensure local directory exists
mkdir -p "$LOCAL_DIR"

# Fetch list of files from S3
FILES=$(aws s3 ls "s3://$S3_BUCKET/$S3_PREFIX" --recursive | awk '{print $4}')

if [ -z "$FILES" ]; then
    echo "No files found in S3 path s3://$S3_BUCKET/$S3_PREFIX"
    exit 1
fi

# Download files from S3
echo "Downloading files from S3..."
for FILE in $FILES; do
    aws s3 cp "s3://$S3_BUCKET/$FILE" "$LOCAL_DIR/"
done

# Transfer files to SFTP
echo "Transferring files to SFTP..."
for LOCAL_FILE in "$LOCAL_DIR"/*; do
    if [ -f "$LOCAL_FILE" ]; then
        echo "Uploading $LOCAL_FILE to SFTP..."
        curl -u "$SFTP_USER:$SFTP_PASSWORD" -T "$LOCAL_FILE" "sftp://$SFTP_HOST$SFTP_DEST_DIR"
    fi
done

# Cleanup local directory
rm -rf "$LOCAL_DIR"
echo "Transfer completed!"
