# router.post("/"),router.get('/') etc are routing logic
# and dynamodb_service.create_employee() is the business logic
from fastapi import APIRouter, HTTPException
from app.models.employee import EmployeeCreate,EmployeeUpdate
from app.services import dynamodb_service

router = APIRouter()

# adding new employee use model as employee.py from models
@router.post("/add-employee")
def add_employee(employee: EmployeeCreate):
    result = dynamodb_service.create_employee(employee)
    return {"message": "Employee added", "employee_id": result}

@router.get("/get-all-employee")
def list_employees():
    return dynamodb_service.get_all_employees()



@router.put("/update-employee/{employee_id}")
def update_employee(employee_id:str,payload: EmployeeUpdate):
    dynamodb_service.update_employee(employee_id,payload.name)
    return {"message": f"Employee {employee_id} updated successfully"}


@router.delete("/delete-employee/{employee_id}")
def delete_employee(employee_id: str):
    dynamodb_service.delete_employee(employee_id)
    return {"message": f"Employee {employee_id} deleted"}

