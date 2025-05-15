# Purpose of Model Testing
# Pydantic models are typically tested to:

# ✅ Ensure validation works correctly (e.g., required fields, data types)

# ✅ Ensure defaults are set properly (like created_time)

# ✅ Ensure edge cases are caught (e.g., missing or invalid values)


from datetime import datetime
from app.models.employee import EmployeeCreate, EmployeeUpdate
import pytest

def test_employee_create_valid():
    emp=EmployeeCreate(employee_id="e123",name="Alice")
    assert emp.employee_id=="e123"
    
    assert emp.name=="Alice"
    
    assert isinstance(emp.created_time,datetime)
    
# This test checks whether Pydantic enforces required fields during model creation.
# This means:

# employee_id is missing.

# name="Alice" is provided.

# created_time is auto-filled (fine).

"""This test checks whether Pydantic enforces required fields during model creation.
    employee_id is required and not provided, Pydantic raises a ValidationError, which inherits 
    from ValueError.So the test will:Pass if Pydantic raises a ValueError due to the missing
    employee_id.
"""   

def test_employee_create_missing_field():
    with pytest.raises(ValueError):
        EmployeeCreate(name="Alice")  # Missing employee_id
        
def test_employee_update_valid():
    emp_update = EmployeeUpdate(name="Bob")
    assert emp_update.name == "Bob"

    
    
    
    