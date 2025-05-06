from fastapi import APIRouter, UploadFile, File, Form, HTTPException,Query
from app.services import yolo_service, s3_service, dynamodb_service_image
from datetime import datetime
import uuid
from typing import Optional
router = APIRouter()

@router.post("/upload")
async def upload_image(employee_id: str = Form(...),file: UploadFile = File(...)):
    # Step 1: Save temporarily & run YOLO
    # This returns the raw content of the file in bytes, not a file path or an image object.
    content=await file.read()
    size = len(content)  # image size in bytes
    tags = yolo_service.detect_objects(content)

    # Step 2: Upload image to S3
    #  If the file was read before (e.g., await file.read() for YOLO), the internal pointer
    #  is at the end.This line resets the pointer to the start so that you can read the file 
    # again (for upload).
    
    file.file.seek(0)  # reset file pointer
    filename = f"{employee_id}/{uuid.uuid4()}.jpg"
    s3_location = s3_service.upload_to_s3(file.file, filename)

    # Step 3: Save metadata to DynamoDB_service_image
    metadata = {
        "employee_id": employee_id,
        "upload_time": datetime.utcnow().isoformat(),
        "s3_location": s3_location,
        "tags": tags,
        "size": size
    }
    dynamodb_service_image.save_image_metadata(metadata)

    return {"message": "Image uploaded", "tags": tags, "s3_location": s3_location}

@router.delete("/image/delete")
def delete_image(employee_id: str, s3_location: str):
    s3_service.delete_from_s3(s3_location)
    dynamodb_service_image.delete_image_metadata(employee_id, s3_location)
    return {"message": "Image deleted successfully"}


# employee_id : It's a simple string; FastAPI handles it automatically

# tags : It's a list, and multiple query values need special parsing

@router.get("/query")
def query_image(employee_id:Optional[str]=None,tags:Optional[list[str]]=Query(None)):
    result=dynamodb_service_image.query_images(employee_id,tags)
    return {"message":result}
