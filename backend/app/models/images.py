from pydantic import BaseModel
from datetime import datetime

class ImageMetadata(BaseModel):
    employee_id: str
    upload_time: str  # ISO formatted string (can be datetime too)
    s3_location: str
    tags: list[str]
    size: int  # in bytes or kilobytes depending on your use case