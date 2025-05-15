# mocking is a great approach for isolating your API tests 
# from the actual backend services like DynamoDB.

# unittest.mock to mock the dynamodb_service functions, so no 
# need to hit the real database.

from fastapi.testclient import TestClient

from unittest.mock import patch

from app.main import app


# TestClient is a tool provided by
# FastAPI (actually from Starlette, which
# FastAPI is built on top of) to let me 
# test  FastAPI app without running a real server.
# TestClient comes from the fastapi.testclient module — which
#  internally wraps around requests to make test HTTP calls.
'''
It creates a test client for FastAPI app.
This client can simulate sending HTTP requests 
(like .get(), .post(), .put(), .delete(), etc.) to routes, as if
a real user or frontend were making them.
'''
client= TestClient(app)

# This is the sample input that I send as the request body (json=) to the /add-employee API.
# It must match the expected Pydantic model in the backend (EmployeeCreate).

sample_employee={
    "employee_id":"emp123",
    "name": "John Doe",
    # This is utc time
    "created_time": "2025-05-11T10:00:00Z"
}

# Here FastAPI route logic is tested:

def test_add_employee():
    mock_data=[sample_employee]
    #  patch: allows to temporarily replace (mock) functions like create_employee during the test.
    '''
    This is the mocking part.Temporarily replaces the create_employee function inside my backend
    with a fake version that just returns 'emp123'.Prevents the test from hitting real DynamoDB
    '''
    with patch("app.API.employee.dynamodb_service.create_employee",return_value='emp123') as mock_create:
        #client Acts like a virtual browser/frontend, but for automated testing.
        # Simulates a real POST request to my FastAPI backend at that route.
        # Sends sample_employee as the request body (json=).
        '''
        Because of the patch, when the FastAPI endpoint calls create_employee(...)
        , it doesn't go to DynamoDB — it just returns 'emp123'.
        '''
        response=client.post("/employees/add-employee",json=sample_employee)
        # Confirms that the request was processed successfully.
        assert response.status_code==200
        # Verifies the returned JSON matches what you expect.
        assert response.json()=={
            "message": "Employee added",
            "employee_id":"emp123"
        }
        # mock_create.assert_called_once() ensures that the mocked 
        # function was called exactly once during the test.
        mock_create.assert_called_once()

def test_list_employees():
    mock_employees = [
        {
            "employee_id": "emp123",
            "name": "John Doe",
            "created_time": "2025-05-04T07:19:17.892000+00:00Z"
        },
        {
            "employee_id": "emp456",
            "name": "Jane Smith",
            "created_time": "2025-05-04T07:20:00.000000+00:00Z"
        }
    ]

    with patch("app.API.employee.dynamodb_service.get_all_employees", return_value=mock_employees) as mock_get:
        response = client.get("/employees/get-all-employee")

        # Check status code
        assert response.status_code == 200

        # Check that the response matches the mocked return value
        assert response.json() == mock_employees

        # Ensure the mock method was called
        mock_get.assert_called_once()
    

def test_update_employee():
    
    employee_id="emp123"
    update_payload={
        "name":"Tanmoy_123"
    }

    with patch ("app.API.employee.dynamodb_service.update_employee",return_value=None) as mock_update:
        response=client.put(f"/employees/update-employee/{employee_id}",json=update_payload)
        assert response.status_code==200
        assert response.json()=={
            "message": f"Employee {employee_id} updated successfully"
            }
        
        # Assert that the mocked function was called with correct args
        mock_update.assert_called_once_with(employee_id,update_payload['name'])
    

def test_delete_employee():
    employee_id="emp123"
    with patch ("app.API.employee.dynamodb_service.delete_employee",return_value=None) as mock_delete:
        response=client.delete(f"/employees/delete-employee/{employee_id}")
        
        assert response.status_code==200
        assert response.json()=={
             "message": f"Employee {employee_id} deleted"
        }
        
        mock_delete.assert_called_once()

# mock_delete.assert_called_once()
# Use this when only care that the function was called exactly once, regardless
# of what arguments it was called with.

# mock_delete.assert_called_once_with(expected_argument)
# Use this when you want to make sure the function was:

# 1) Called exactly once

# 2) Called with the exact argument(s) you expect

    





    


























