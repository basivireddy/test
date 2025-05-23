import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    for record in event['Records']:
        body = json.loads(record['body'])

        # For simple message
        bucket = body['bucket']
        key = body['key']

        # For S3 notification via SQS
        # s3_info = json.loads(record['body'])['Records'][0]['s3']
        # bucket = s3_info['bucket']['name']
        # key = s3_info['object']['key']

        print(f"Reading from S3: bucket={bucket}, key={key}")
        
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')

        print("S3 Data:", data)

        # Further processing logic...

    return {"status": "done"}
