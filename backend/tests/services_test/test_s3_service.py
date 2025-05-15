import io
from unittest.mock import patch,MagicMock
from app.services import s3_service

def test_upload_to_s3():
    fake_file = io.BytesIO(b"fake image data")

    with patch("app.services.s3_service.s3.upload_file") as mock_upload_file, \
         patch("app.services.s3_service.tempfile.NamedTemporaryFile") as mock_tempfile, \
         patch("app.services.s3_service.os.remove") as mock_remove:
             
        
        # Creates a mock object (mock_temp) that simulates the temporary file 
        # object returned by NamedTemporaryFile().
        mock_temp = MagicMock()
        
        # Assigns a fake file name to the `.name` attribute of `mock_temp`, mimicking
        # what a real temporary file would have.
        mock_temp.name = "/fake/temp.jpg"
        
        # Set this mock as the return value of the context manager
        # mocking a context manager
        # That object’s __enter__() method is called when the with block begins.
        # You're setting __enter__.return_value to mock_temp — which means temp
        # inside the with block becomes mock_temp
        mock_tempfile.return_value.__enter__.return_value = mock_temp

        # Call the function
        result = s3_service.upload_to_s3(fake_file, "test.jpg")

        # Assert correct call
        mock_upload_file.assert_called_once_with(
            "/fake/temp.jpg", "alpha-ai-new", "Oudarja_Barman_Tanmoy/test.jpg"
        )


def test_delete_from_s3():
    with patch("app.services.s3_service.s3.delete_object") as mock_delete:
        s3_service.delete_from_s3("alpha-ai-new/Oudarja_Barman_Tanmoy/test.jpg")
        mock_delete.assert_called_once_with(
            Bucket="alpha-ai-new",
            Key="Oudarja_Barman_Tanmoy/test.jpg"
        )
