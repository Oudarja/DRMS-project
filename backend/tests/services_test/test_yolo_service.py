import pytest
from app.services.yolo_service import detect_objects

# with open("tests/services_test/sample_image/cat2.jpg", "rb") as img_file:
# passes because I am running pytest from the 'backend' directory: so if I 
# don't start opening from tests pytest is not able to find this 

def test_detect_objects_returns_labels():
    # Load a sample image (make sure the image exists)
    with open("tests/services_test/sample_image/cat2.jpg", "rb") as img_file:
        image_bytes = img_file.read()

    # Call the object detection function
    labels = detect_objects(image_bytes)
    
    print(labels)

    # Check type and structure
    assert isinstance(labels, list)
    assert all(isinstance(label, str) for label in labels)

    # Optional: You can test for expected classes if image is known (e.g., "dog", "person")
    assert len(labels) > 0  # Should detect at least one object


