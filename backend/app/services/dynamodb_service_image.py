# Business logic for DynamoDB
# These are called from your API routers in api/employee.py, api/image.py, etc.
from dotenv import load_dotenv
import os
import boto3
from datetime import datetime
from app.models.employee import EmployeeCreate
from app.models.images import  ImageMetadata
# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

# Create DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=aws_region
)

# Use the table
table = dynamodb.Table('team-alpha-ai')

user_id = "Tanmoy_images"

def save_image_metadata(metadata: dict):
     # Optional: Validate and convert dict to Pydantic model
     validated_metadata = ImageMetadata(**metadata)
     response = table.get_item(Key={'id': user_id})
     
     # Check if the 'Item' exists in the response
     if 'Item' not in response:
        # If no item exists, initialize an empty employee list for the user
        item = {'id': user_id, 'images_data': []}
     else:
        # If item exists, use the existing employee data
        item = response['Item']
    
     image_metadata=item['images_data']

     image_metadata.append(validated_metadata.dict())

     table.put_item(Item={
        'id': user_id,  # Use your table's partition key
        'images_data':image_metadata   # Could act as sort key if defined
        })
     return validated_metadata.dict()

# Delete image bussiness logic 
def delete_image_metadata(employee_id:str, s3_location:str):
   response = table.get_item(Key={'id': user_id})

   if 'Item' not in response:
        raise ValueError("Employee ID not found in database")

   item = response['Item']
   images_data = item.get('images_data', [])
   # Filter out the entry with the matching s3_key
   updated_images = [img for img in images_data if img["s3_location"] != s3_location]

   # Put updated item back
   table.put_item(Item={
        'id': user_id,
        'images_data': updated_images
   })















    
    

    




