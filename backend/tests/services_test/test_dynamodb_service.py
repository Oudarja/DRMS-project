# moto
# A mocking library specifically for AWS services.

# It allows you to test your code that interacts with
# AWS (like S3, DynamoDB, etc.) without actually calling AWS.

# Example: By uaing moto can be  created a fake S3 bucket or DynamoDB table
# in memory for testing

import pytest
from unittest.mock import patch, MagicMock
from app.services import dynamodb_service
from app.models.employee import EmployeeCreate
from datetime import datetime

# This function creates a dummy employee using the EmployeeCreate
# model (probably a Pydantic model). pytest will run this function
# before any test that uses it as an argument.

@pytest.fixture
def sample_employee():
    return EmployeeCreate(
        employee_id="E999",
        name="Test Employee",
        created_time=datetime.utcnow()
    )

# whenever dynamodb_service.table is used in this test, replace
# it with a mock object called mock_table, Pass that mock into 
# the test function as the first argument — named mock_table
#  The sample_employee in test function is a pytest fixture, which
# is automatically injected by pytest when running the test.

@patch("app.services.dynamodb_service.table")
def test_create_employee(mock_table, sample_employee):
    
    # Simulates that the employee doesn't already exist (get_item returns empty).
    # # put_item also does nothing, just simulates success.
    
    # Mock table.get_item to simulate item not existing initially
    mock_table.get_item.return_value = {}

    # Mock table.put_item
    mock_table.put_item.return_value = {}
    
    # You're testing your real create_employee() function.
    # It interacts with table, but that table is now a mock
    # (mock_table), so no actual AWS calls are made.

    emp_id = dynamodb_service.create_employee(sample_employee)

    assert emp_id == sample_employee.employee_id
    
    mock_table.put_item.assert_called_once()
    

@patch("app.services.dynamodb_service.table")
def test_get_all_employees(mock_table):
    mock_table.get_item.return_value = {
        "Item": { 
            "employee": [
                {
                    "employee_id": "E001",
                    "name": "Alice",
                    "created_time": "2024-05-13T12:34:56Z" 
                }
                ]
            }
        }

    result = dynamodb_service.get_all_employees()
    
    # Assertions – Validating Output
    assert isinstance(result, list)
    # return a list and from that access the 1st eleement
    assert result[0]["employee_id"] == "E001"


@patch("app.services.dynamodb_service.table")
def test_update_employee(mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "employee": [{"employee_id": "E123", "name": "Old Tanmoy"}]
        }
    }

    dynamodb_service.update_employee("E123", "New Tanmoy")
    mock_table.put_item.assert_called_once()
    # mock_table.put_item.call_args returns a tuple:(positional_args, keyword_args)
    # mock_table.put_item.call_args == ((), {'Item': {...}})
    # call_args[0] → () → positional args
    # call_args[1] → {'Item': {...}} → keyword args
    # mock_table.put_item.call_args[1] == mock_table.put_item.call_args.kwargs

    updated_data = mock_table.put_item.call_args[1]["Item"]["employee"]
    
    assert updated_data[0]["name"] == "New Tanmoy"


# unittest.mock.patch to mock the services and interactions with DynamoDB and S3
# @patch("app.services.dynamodb_service.table"): This decorator replaces the table 
# (DynamoDB table) object in dynamodb_service with a mock object (mock_table) during the test.

# @patch("app.services.dynamodb_service.s3_service"): Similarly, this mocks the S3 service to
# avoid real interactions with AWS during testing, replacing s3_service with mock_s3_service.


@patch("app.services.dynamodb_service.table")
@patch("app.services.dynamodb_service.s3_service")
def test_delete_employee(mock_s3_service, mock_table):
    # Set up sample data
    emp_id_to_delete = "E001"

    # This is the employee metadata stored under 'Tanmoy'
    employee_data = {
        "Item": {
            "employee": [
                {"employee_id": "E001", "name": "Alice"},
                {"employee_id": "E002", "name": "Bob"},
            ]
        }
    }

    # This is the image metadata stored under 'Tanmoy_images'
    image_data = {
        "Item": {
            "images_data": [
                {"employee_id": "E001", "s3_location": "s3://bucket/image1.jpg"},
                {"employee_id": "E002", "s3_location": "s3://bucket/image2.jpg"},
            ]
        }
    }

    # Mock the get_item return values
    
    # [[ When this line executes inside delete_employee:
    #    response = table.get_item(Key={'id': "Tanmoy"})
    
    # Then this line:response_img = table.get_item(Key={'id': "Tanmoy_images"})
    # mock_get_item({"id": "Tanmoy_images"}) is automatically invoked and returns image_data.]]
    
    def mock_get_item(Key):
        if Key["id"] == "Oudarja_Tanmoy":
            return employee_data
        elif Key["id"] == "Tanmoy_images":
            return image_data
        
    
    # This tells the mock:"Hey mock_table.get_item, whenever
    # you're called, do not behave like a normal mock — instead, call 
    # this function mock_get_item(Key) and return whatever it returns.
    

    mock_table.get_item.side_effect = mock_get_item

    # Call the function
    dynamodb_service.delete_employee(emp_id_to_delete)

    # Verify S3 deletion called for E001
    # This asserts that delete_from_s3 was called exactly once with the correct
    # S3 location of Alice's image ("s3://bucket/image1.jpg"). This ensures that 
    # the image was deleted from the S3 bucket.
    mock_s3_service.delete_from_s3.assert_called_once_with("s3://bucket/image1.jpg")

    # Verify put_item was called to update both tables
    expected_employee_list = [{"employee_id": "E002", "name": "Bob"}]
    expected_image_list = [{"employee_id": "E002", "s3_location": "s3://bucket/image2.jpg"}]
    
    # This verifies that put_item was called with the correct arguments to update both tables
    # verify that a mocked method was called at least once with the specified arguments
    mock_table.put_item.assert_any_call(Item={
        "id": "Oudarja_Tanmoy",
        "employee": expected_employee_list
    })

    mock_table.put_item.assert_any_call(Item={
        "id": "Tanmoy_images",
        "images_data": expected_image_list
    })

    assert mock_table.put_item.call_count == 2



    









