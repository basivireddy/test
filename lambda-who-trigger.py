import json

def lambda_handler(event, context):
    print("Event: ", json.dumps(event, indent=2))
    
    # Identify trigger source
    if "Records" in event:
        if "s3" in event["Records"][0]:
            print("Triggered by S3")
        elif "sns" in event["Records"][0]:
            print("Triggered by SNS")
        elif "dynamodb" in event["Records"][0]:
            print("Triggered by DynamoDB")
        elif "eventSource" in event["Records"][0] and event["Records"][0]["eventSource"] == "aws:sqs":
            print("Triggered by SQS")
    
    elif "source" in event and event["source"] == "aws.events":
        print("Triggered by EventBridge (Scheduled Event)")
    
    elif "httpMethod" in event:
        print("Triggered by API Gateway")
    
    elif "requestContext" in event and "http" in event["requestContext"]:
        print("Triggered by AWS HTTP API Gateway (V2)")
    
    else:
        print("Unknown trigger")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully!')
    }
