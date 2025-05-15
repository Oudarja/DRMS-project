# Imports TestClient, which allows you to test your FastAPI app without actually running a server.
from fastapi.testclient import TestClient
# patch is used to mock (simulate) external service calls—great for isolating your test logic.
from unittest.mock import patch
from app.main import app
import io

# unittest.mock.patch to mock external services like YOLO, S3, and DynamoDB.
client= TestClient(app)

# Mock data for testing
mock_tags = ["tag1", "tag2"]
mock_s3_location = "s3://bucket/employee1/uuid.jpg"
mock_metadata = {
    "employee_id": "emp123",
    "upload_time": "2025-05-12T10:00:00Z",
    "s3_location": mock_s3_location,
    "tags": mock_tags,
    "size": 1024,
}

def test_upload_image():
    employee_id = "emp123"
    # Creating the mock file directly inside the test
    file_content = b"fake_image_content"
    file = io.BytesIO(file_content)
    file.filename = "image.jpg"

    with patch("app.API.image.yolo_service.detect_objects", return_value=mock_tags) as mock_detect_objects, \
         patch("app.API.image.s3_service.upload_to_s3", return_value=mock_s3_location) as mock_upload_to_s3, \
         patch("app.API.image.dynamodb_service_image.save_image_metadata", return_value=mock_metadata) as mock_save_metadata:

        response = client.post(
            "/images/upload",
            files={"file": ("image.jpg", file, "image/jpeg")},
            data={"employee_id": employee_id}
        )

        assert response.status_code == 200
        assert response.json() == {
            "message": "Image uploaded",
            "tags": mock_tags,
            "s3_location": mock_s3_location
        }

        # Adjust the mock call expectation to match the file content
        mock_detect_objects.assert_called_once_with(file_content)
        mock_upload_to_s3.assert_called_once()
        mock_save_metadata.assert_called_once()
        


def test_delete_image():
    employee_id = "emp1"
    with patch("app.API.image.s3_service.upload_to_s3", return_value=mock_s3_location) as mock_upload_to_s3, \
        patch("app.API.image.dynamodb_service_image.delete_image_metadata",return_value=None) as mock_save_metadata:
            
        response = client.delete(
            "/images/image/delete",
            params={"employee_id": employee_id, "s3_location": mock_s3_location}
        )
        
        assert response.status_code==200
        
        assert response.json()=={
            "message": "Image deleted successfully"
        }
        

def test_query_image():
     mock_urls = [
        "https://s3.amazonaws.com/bucket/image1.jpg?sig=abc",
        "https://s3.amazonaws.com/bucket/image2.jpg?sig=xyz"
    ]
     with patch("app.API.image.dynamodb_service_image.query_images", return_value=mock_urls) as mock_query:
         response = client.get("/images/query", params={
            "employee_id": "emp123",
            "tags": ["tag1", "tag2"]
            })
         assert response.status_code == 200
         assert response.json() == {"message": mock_urls}
         mock_query.assert_called_once_with("emp123", ["tag1", "tag2"])
    
    

    
    



