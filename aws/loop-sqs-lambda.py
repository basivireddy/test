import boto3
import json
import os

# Create SQS client
sqs = boto3.client('sqs', region_name="us-west-2")  # Change region if needed

# Set your SQS Queue URL
QUEUE_URL = os.environ.get("QUEUE_URL", "https://sqs.us-west-2.amazonaws.com/043309350086/my-sqs-queue")

def lambda_handler(event, context):
    print("event:",event)
    if "Records" in event:
        print("Received event from SQS")
        for record in event['Records']:
           body = record['body']
           print(f'Received message from SQS: {body}')

            # Delete message from queue after processing
           sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=record["receiptHandle"]
           )
           print("Message deleted\n")


    message_body = {
        "order_id": "12345",
        "status": "pending",
        "customer": "John Doe"
    }

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message_body),
        DelaySeconds=60
    )

    print(response)
    print("Message Sent! MessageId:", response["MessageId"])

    return {
        "statusCode": 200,
        "body": json.dumps("Message sent to SQS!")
    }


