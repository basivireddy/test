import boto3
import os

# Initialize SNS client
sns_client = boto3.client('sns')

# Environment variable for SNS Topic ARN (Recommended)
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:MySNSTopic")

def lambda_handler(event, context):
    message = "Hello from Lambda!"
    
    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Lambda to SNS Test"
    )
    
    return {
        "statusCode": 200,
        "body": f"Message sent! Message ID: {response['MessageId']}"
    }
