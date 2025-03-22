import boto3
import json
import os

# Create SQS client
sqs = boto3.client('sqs', region_name="us-east-1")  # Change region if needed

# Set your SQS Queue URL
QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue")

def lambda_handler(event, context):

    response = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=["ApproximateNumberOfMessagesNotVisible"]
    )
    in_flight_count = response["Attributes"]["ApproximateNumberOfMessagesNotVisible"]
    print(f"Messages in flight: {in_flight_count}")
    
    message_body = {
        "order_id": "12345",
        "status": "pending",
        "customer": "John Doe"
    }

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )

    print(response)
    print("Message Sent! MessageId:", response["MessageId"])


    read_response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=5,  # Get up to 5 messages
        WaitTimeSeconds=10  # Long polling
    )

    if "Messages" in read_response:
        for message in read_response["Messages"]:
            print("Received message:", message["Body"])

            # Process message logic goes here

            # Delete message from queue after processing
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"]
            )
            print("Message deleted\n")
    else:
        print("No messages in queue")
        
    return {
        "statusCode": 200,
        "body": json.dumps("Message sent to SQS!")
    }



