import pytest
from unittest.mock import patch
from app.services import dynamodb_service_image

# Sample test data
image_metadata = {
    "employee_id": "E001",
    "s3_location": "alpha-ai-new/images/img1.jpg",
    "size": 333161,
    "tags": ["face", "entry"],
    "upload_time": "2024-05-01T10:00:00"
}

@patch("app.services.dynamodb_service_image.table")
def test_save_image_metadata(mock_table):
    # Simulate no existing entry
    mock_table.get_item.return_value = {}
    
    saved = dynamodb_service_image.save_image_metadata(image_metadata)
    
    assert saved == image_metadata
    
    mock_table.put_item.assert_called_once()
    
    # args has kwargs (keyword argument) passed into mock_table
    # now inspection on that argument will be done 
    args = mock_table.put_item.call_args[1]
    assert args["Item"]['id']=="Tanmoy_images"
    # args["Item"]['images_data'] is a list so == can not be used
    assert saved in args["Item"]['images_data']

@patch("app.services.dynamodb_service_image.table")
def test_delete_image_metadata(mock_table):
    employee_id= "E001"
    s3_location= "alpha-ai-new/images/img1.jpg"
    mock_table.get_item.return_value = {
        "Item": {
            "images_data": [image_metadata]
        }
    }
    dynamodb_service_image.delete_image_metadata(employee_id, s3_location)
    mock_table.put_item.assert_called_once()
    args = mock_table.put_item.call_args[1]
    assert len(args["Item"]["images_data"]) == 0  # Image should be deleted
    

@patch("app.services.dynamodb_service_image.s3_client")
def test_generate_presigned_url(mock_s3_client):
    mock_s3_client.generate_presigned_url.return_value = "https://signed-url"

    result = dynamodb_service_image.generate_presigned_url("images/img1.jpg")
    assert result == "https://signed-url"

# When using multiple @patch decorators, the **order of the function arguments is
# reversed from the order of the decorators.

mock_generate_presigned_url = patch("app.services.dynamodb_service_image.generate_presigned_url")
mock_table = patch("app.services.dynamodb_service_image.table")

@mock_table
@mock_generate_presigned_url
def test_query_images_by_tags(mock_url, mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "images_data": [image_metadata]
        }
    }

    mock_url.return_value = "https://presigned-url"

    result = dynamodb_service_image.query_images(tags=["entry"])
    # result is a list of url of image matched to given tags
    assert "https://presigned-url" in result
    mock_url.assert_called_once()
    
    

@patch("app.services.dynamodb_service_image.table")
@patch("app.services.dynamodb_service_image.generate_presigned_url")
def test_query_images_by_employee(mock_url, mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "images_data": [image_metadata]
        }
    }

    mock_url.return_value = "https://presigned-url"

    result = dynamodb_service_image.query_images(employee_id="E001")
    assert "https://presigned-url" in result
    mock_url.assert_called_once()

