# These are all bussiness logic
# Business logic for S3
# Business logic is the part of your codebase that handles the core operations and rules 
# of your application — how data is processed, stored, or computed.
import boto3
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=aws_region
)


# Upload file
def upload_to_s3():
    # s3.upload_file(local_file_path, bucket_name, s3_folder)
    s3.upload_file("example.jpg", "alpha-ai-new", "Oudarja_Barman_Tanmoy/example.jpg")