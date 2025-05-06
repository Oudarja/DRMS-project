# Business logic for object detection
from ultralytics import YOLO
import tempfile
import os


# Load YOLO model only once (at module level)
model = YOLO("yolov8n.pt")

def detect_objects(image_bytes: bytes) -> list[str]:
    '''
    ->tempfile is used to temporarily save the uploaded file in memory before passing it to YOLO.
    ->model = YOLO("yolov8n.pt") is placed at the module level so it doesn’t reload every time.
    ->Returns a list of unique class names (e.g., ["person", "dog"]).
    '''
    # Save image temporarily for detection
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
        # Write the incoming image data (image_bytes, likely from UploadFile.read())
        # into the temporary file.
        # YOLO needs to load images from disk (by path), so we need to save the bytes first.
        temp_image.write(image_bytes)
        # Purpose: Ensure all written data is physically saved to disk.
        # This is critical — without this, YOLO might read an incomplete or empty file if the
        #  buffer wasn't flushed yet.
        temp_image.flush()

        # Run detection on saved image
        # YOLOv8 runs inference (object detection) on the temp image.
        # results contains bounding boxes, class IDs, confidence scores, etc.
        # Run YOLOv8 model inference on the image saved at temp_image.name (the file path).
    results = model(temp_image.name,conf=0.1)
     # Optionally delete manually
    os.remove(temp_image.name)

    detected_classes = set()  # Use set to avoid duplicates
     # Loop through results to collect class names
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = result.names[class_id]
            detected_classes.add(class_name)
        
    # Converts the set of class names to a list before returning it.
    return list(detected_classes)

'''
The Ultralytics YOLO model expects:

A file path (str), or

A NumPy array or PIL image.

But FastAPI gives you bytes, so you need to:

Temporarily save the bytes to a file using tempfile.NamedTemporaryFile, or

Convert the bytes into a NumPy array or image directly in memory (without saving).

You're currently using Option 1 for simplicity.
'''