from pydantic import BaseModel, Field
from datetime import datetime

# Field(...) is used for:
# Setting default values (with default or default_factory)
# Adding validation constraints (like min_length, max_length, gt, lt, etc.)
# Adding metadata (like a description or title for documentation)
# default_factory=datetime.utcnow sets a dynamic default value at runtime (e.g., for timestamps).

class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    created_time:datetime = Field(default_factory=datetime.utcnow)

class EmployeeUpdate(BaseModel):
    name: str