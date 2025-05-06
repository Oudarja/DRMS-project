# Business logic for DynamoDB
# These are called from your API routers in api/employee.py, api/image.py, etc.
from dotenv import load_dotenv
import os
import boto3
from datetime import datetime
from app.models.employee import EmployeeCreate
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

user_id = "Oudarja_Tanmoy"

# Create item (C)
 # employee_info = [
    #     {'employee_id': 'E000',
    #     'name': 'Charlie',
    #     'created_at': datetime.utcnow().isoformat() + 'Z'
    #     }
    #     ]

def create_employee(employee:EmployeeCreate):
    response = table.get_item(Key={'id': user_id})

    # Check if the 'Item' exists in the response
    if 'Item' not in response:
        # If no item exists, initialize an empty employee list for the user
        item = {'id': user_id, 'employee': []}
    else:
        # If item exists, use the existing employee data
        item = response['Item']

    employee_data=item['employee']
    # ✅ Convert Pydantic model to dictionary
    employee_dict = employee.dict()  
    employee_dict['created_time'] = employee_dict['created_time'].isoformat() + 'Z'
    employee_data.append(employee_dict)

    table.put_item(Item={
        'id': user_id,  # Use your table's partition key
        'employee':employee_data   # Could act as sort key if defined
        })
    return employee_dict['employee_id']


    
# Read (R)
def get_all_employees():
    response = table.get_item(Key={'id': user_id})
    item = response.get('Item')
    # print(item,user_id)
    if item:
        # item['employee'] or item.get('employee')
        employee_data = item['employee']
        print("READ item:", employee_data)
        return employee_data
    else:
        print("Item not found.")

# Update
# How update will work that has to be maintained 
# later like if an admin upload an image again(first uploaded) against a employee
# then again the metadata field of employee has to be updated by adding new mwtadat with
# the previous one , and option should also be here to edit the name of employee.
# When a function has optional arguments, always use keyword arguments for clarity 
# and correctness.

def update_employee(emp_id,name):
    
    response = table.get_item(Key={'id': user_id})

    item=response['Item']

    employee_data=item['employee']

    for i in employee_data:
        if i['employee_id']==emp_id:
            # Update name if provided
            if name:
                i['name'] = name
            
            # # Update name if provided
            # if new_meta_data:
            #     i['metadata'].extend(new_meta_data)
            
            # # store only the unique 
            # i['metadata']=list(i['metadata'])
    
    table.put_item(Item={
        'id': user_id,  # Use your table's partition key
        'employee': employee_data # Could act as sort key if defined
        })


# Delete
'''
You're trying to get 'employee' directly from the response, but boto3 
returns the item like this:
{
  'Item': {
    'id': 'Oudarja_Tanmoy',
    'employee': [...]
  }
}

'''
# Delete a specific employee following it's id
def delete_employee(emp_id):
    response = table.get_item(Key={'id': user_id})
    item = response.get('Item')

    # This is list of dicts
    employees = item['employee']

    # linear search to find 
    # optimization purpose BS can be used later
    updated_employee_list = []
    
    for i in employees:
        if i['employee_id']!=emp_id:
            updated_employee_list.append(i)

    table.put_item(Item={
        'id': user_id,  # Use your table's partition key
        'employee': updated_employee_list   # Could act as sort key if defined
        })

    print("DELETE response:", response)

