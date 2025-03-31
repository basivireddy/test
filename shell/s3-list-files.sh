#!/bin/bash

# Set your S3 bucket and folder
BUCKET_NAME="your-bucket-name"
FOLDER_PREFIX="your-folder-name/"  # Ensure it ends with a slash

# List all files in the S3 folder
FILES=$(aws s3 ls "s3://$BUCKET_NAME/$FOLDER_PREFIX" --recursive | awk '{print $4}')

# Check if any files were found
if [ -z "$FILES" ]; then
    echo "No files found in S3 folder: s3://$BUCKET_NAME/$FOLDER_PREFIX"
    exit 1
fi

# Loop through each file and count lines
for FILE in $FILES; do
    echo "Processing: $FILE"
    LINE_COUNT=$(aws s3 cp "s3://$BUCKET_NAME/$FILE" - | wc -l)
    echo "File: $FILE, Lines: $LINE_COUNT"
done
