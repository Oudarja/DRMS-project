# These are all bussiness logic
# Business logic for S3
# Business logic is the part of your codebase that handles the core operations and rules 
# of your application — how data is processed, stored, or computed.
import boto3
from dotenv import load_dotenv
import os
import tempfile

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


# # Upload file
# def upload_to_s3():
#     # s3.upload_file(local_file_path, bucket_name, s3_folder)
#     # s3.upload_file("example.jpg", "alpha-ai-new", "Oudarja_Barman_Tanmoy")

def upload_to_s3(file_obj, filename):
    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(file_obj.read())
        temp_path = temp.name

    # Create full key/path inside the bucket
    s3_key = f"Oudarja_Barman_Tanmoy/{filename}"

    try:
        # Upload to S3
        s3.upload_file(temp_path,"alpha-ai-new", s3_key)
    except Exception as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")
    finally:
        # Clean up the temp file
        os.remove(temp_path)

    # Return the S3 location (not a URL)
    return f"alpha-ai-new/{s3_key}"

# delete image bussiness logic from s3 
def delete_from_s3(s3_location: str):
    s3_location_stripped = s3_location[len("alpha-ai-new/"):]
    s3.delete_object(Bucket="alpha-ai-new",Key=s3_location_stripped)

