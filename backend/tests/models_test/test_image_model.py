import pytest
from app.models.images import ImageMetadata 

def test_image_metadata_valid():
    metadata = ImageMetadata(
        employee_id="E001",
        upload_time="2024-12-01T12:00:00Z",
        s3_location="s3://bucket/image1.jpg",
        tags=["yolo", "person", "car"],
        size=2048
    )
    assert metadata.employee_id == "E001"
    assert metadata.upload_time.startswith("2024-12-01")
    assert metadata.s3_location.endswith(".jpg")
    assert "person" in metadata.tags
    assert metadata.size == 2048

# Intentionally make missing of tags and size 
def test_image_metadata_missing_field():
    with pytest.raises(ValueError):
        ImageMetadata(
            employee_id="E001",
            upload_time="2024-12-01T12:00:00Z",
            s3_location="s3://bucket/image1.jpg",
            # missing tags and size
        )

# Intentionally make mis match in type
def test_image_metadata_type_change():
    with pytest.raises(ValueError):
        ImageMetadata(
            employee_id="E001",
            upload_time="2024-12-01T12:00:00Z",
            s3_location="s3://bucket/image1.jpg",
            tags=["yolo"],
            # size should have to be int but here given string so this is type mis match with pydantic 
            # model that has been defined already .
            size="two thousand"  
        )