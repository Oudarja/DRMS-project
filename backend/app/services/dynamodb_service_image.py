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

s3_bucket_name=os.getenv("S3_BUCKET_NAME")


# Create DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=aws_region
)

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_key,        # Replace with your access key
    aws_secret_access_key=aws_secret,    # Replace with your secret key
    region_name=aws_region                     # Your bucket's region
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
# To delete a specific image of an employee
# An employee can have many image uploaded, but if when anyone  
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


'''
'get_object'	 Generate a URL to download (GET) a file
'put_object'	 Generate a URL to upload (PUT) a file
'delete_object' Generate a URL to delete an object
'list_objects'	 List contents of a bucket (rare in presign)
'''

def generate_presigned_url(object_key, expiration=60):
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': "alpha-ai-new", 'Key': object_key},
            ExpiresIn=expiration  # Time in seconds (default: 3600 = 1 hour)
        )
        return url
    except Exception as e:
        print("Error generating pre-signed URL:", e)
        return object_key

# Very bulky and time consuming function complexity can be optimized 
# later for searching using BS


# if employee_id is here then check for tags of that specific if no tags then just return image of 
# that specific employee_id , if tags are here then for each object that match the employee id ,search 
# each object match for tags if any tag maches then return image of that employeeid's image
# else only tags then search each object match for tags if any tag maches then return image of that
#  employeeid's image
def query_images(employee_id: str = None, tags: list[str] = None):
    # Fetch employee record from DynamoDB
    response = table.get_item(Key={'id': user_id})
    if 'Item' not in response:
        raise ValueError("Employee ID not found in database")

    item = response['Item']
    images_data = item.get('images_data', [])
    matched_locations = set()

    tags_lower = {tag.lower() for tag in tags} if tags else set()

    for obj in images_data:
        obj_emp_id = obj.get('employee_id')
        obj_tags = obj.get('tags', [])
        obj_tags_lower = {tag.lower() for tag in obj_tags}

        if employee_id:
            if obj_emp_id != employee_id:
                continue  # skip irrelevant employees
            if tags_lower:
                for i in tags_lower:
                    for j in obj_tags_lower:
                        if i==j:
                            matched_locations.add(obj.get('s3_location'))
            else:
                matched_locations.add(obj.get('s3_location'))
        elif tags_lower:
             for i in tags_lower:
                    for j in obj_tags_lower:
                        if i==j:
                            matched_locations.add(obj.get('s3_location'))

    urls = [
        generate_presigned_url(s3_path.replace('alpha-ai-new/', ''))
        for s3_path in matched_locations
    ]
    return urls










   


   

      
   
   





















    
    

    




