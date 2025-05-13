import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        
        # Simple call to check connectivity - list buckets
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        
        logger.info(f"Successfully connected to S3. Buckets: {bucket_names}")
        return {
            'statusCode': 200,
            'body': f"Connected to S3. Buckets: {bucket_names}"
        }
        
    except Exception as e:
        logger.error(f"Error connecting to S3: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Failed to connect to S3: {str(e)}"
        }
