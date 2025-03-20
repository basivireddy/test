import boto3
import json

# Create SQS client
sqs = boto3.client('sqs', region_name='us-east-1')  # Change region if needed

# Replace with your queue URL
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue"

def read_messages():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,  # Read up to 10 messages at a time
        WaitTimeSeconds=10  # Long polling to reduce empty responses
    )

    if 'Messages' in response:
        for message in response['Messages']:
            print("Message Body:", message['Body'])

            # Delete the message after processing
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
            print("Message deleted\n")
    else:
        print("No messages in queue")

# Run the function
read_messages()
