Got it — you want to check via Python if S3 traffic is going through the VPC Gateway Endpoint instead of a proxy.

Here’s a minimal example using boto3 + socket to see if the resolved S3 hostname is private (VPC endpoint) or public (proxy/NAT):

import boto3
import socket
import ipaddress

# Your AWS region
REGION = "us-east-1"

# Create an S3 client
s3 = boto3.client("s3", region_name=REGION)

# The standard S3 endpoint hostname
hostname = f"s3.{REGION}.amazonaws.com"

# Resolve to IP
ip_address = socket.gethostbyname(hostname)

# Check if it's private
is_private = ipaddress.ip_address(ip_address).is_private

print(f"S3 endpoint resolves to: {ip_address}")
if is_private:
    print("✅ Traffic is likely going through the VPC Gateway Endpoint.")
else:
    print("⚠ Traffic is going through public network (proxy/NAT).")


⸻

How this works
	•	If you have a VPC Gateway Endpoint, AWS DNS returns a private IP in the VPC range (e.g., 10.x.x.x).
	•	If it’s going through a proxy/NAT, you’ll get a public AWS S3 IP.

⸻

Extra: Force a real S3 call and see the connection

If you want to be 100% sure, you can run a small S3 request and log the connection:

from botocore.config import Config

config = Config(region_name=REGION)
response = s3.list_buckets(Config=config)
print("Buckets:", [b['Name'] for b in response['Buckets']])

Then check VPC Flow Logs or enable boto3.set_stream_logger('botocore') to see connection details.

⸻

If you want, I can extend this script so it actually runs an S3 request and confirms the source/destination IP from inside Python without checking flow logs. That would be a direct proof of endpoint usage. Would you like me to do that?