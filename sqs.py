import json
import boto3
import os

# Initialize SQS client
sqs = boto3.client('sqs')

# Get SQS queue URL from environment variables
QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

def lambda_handler(event, context):
    try:
        # Example message body (modify as needed)
        message_body = json.dumps({"message": "Hello from Lambda!", "event": event})

        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=message_body
        )

        # Log message ID for debugging
        print(f"Message sent to SQS with ID: {response['MessageId']}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Message sent successfully!", "MessageId": response['MessageId']})
        }

    except Exception as e:
        print(f"Error sending message to SQS: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
