#!/bin/bash

# Variables
BUCKET="your-bucket-name"
KEY="path/to/yourfile.csv"

# Download first line (header) from CSV and count columns
header=$(aws s3 cp s3://$BUCKET/$KEY - | head -n 1)

# Assuming CSV is comma-separated, count columns
column_count=$(echo "$header" | tr -cd ',' | wc -c)
total_columns=$((column_count + 1))

echo "Total number of columns: $total_columns"


#!/bin/bash

# Path to your local CSV file
FILE="yourfile.csv"

# Read the first line (header)
header=$(head -n 1 "$FILE")

# Count commas
column_count=$(echo "$header" | tr -cd ',' | wc -c)

# Total columns = commas + 1
total_columns=$((column_count + 1))

echo "Total number of columns: $total_columns"
