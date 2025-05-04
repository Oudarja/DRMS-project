from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import yolo_service, s3_service, dynamodb_service_image
from datetime import datetime


router = APIRouter()

@router.post("/upload")
async def upload_image(employee_id: str = Form(...),file: UploadFile = File(...)):
    # Step 1: Save temporarily & run YOLO
    # This returns the raw content of the file in bytes, not a file path or an image object.
    tags = yolo_service.detect_objects(await file.read())

    # Step 2: Upload image to S3
    #  If the file was read before (e.g., await file.read() for YOLO), the internal pointer
    #  is at the end.This line resets the pointer to the start so that you can read the file 
    # again (for upload).
    
    file.file.seek(0)  # reset file pointer
    filename = f"{employee_id}/{uuid.uuid4()}.jpg"
    s3_url = s3_service.upload_to_s3(file.file, filename)

    # Step 3: Save metadata to DynamoDB
    metadata = {
        "image_id": str(uuid.uuid4()),
        "employee_id": employee_id,
        "upload_time": datetime.utcnow().isoformat(),
        "s3_url": s3_url,
        "tags": tags
    }
    dynamodb_service.save_image_metadata(metadata)

    return {"message": "Image uploaded", "tags": tags, "s3_url": s3_url}





