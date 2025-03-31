#!/bin/bash

# Set your S3 bucket and folder
BUCKET_NAME="your-bucket-name"
FOLDER_PREFIX="your-folder-name/"  # Ensure it ends with a slash

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


# Loop through dictionary keys & values
echo "list files and count"
for key in "${!files_dict[@]}"; do
    echo "$key: ${files_dict[$key]}"
done

return files_dict
