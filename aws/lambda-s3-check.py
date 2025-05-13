import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'your-bucket-name'
    prefix = 'your/path/prefix/'  # e.g., 'folder/subfolder/' (include trailing slash if needed)

    files = []
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                files.append(obj['Key'])

    return {
        'statusCode': 200,
        'body': files  # You can serialize to JSON if needed
    }
