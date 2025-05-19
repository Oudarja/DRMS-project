# DRMS - Digital Resource Management System

A secure, cloud-based document and resource(image corresponding each employee and employee information) management system designed for internal use where only the **admin** has access to manage employee records and upload associated images. Built with modern technologies using MVC (Model , View , Controll) pattern , scalable architecture.

---

## Features

-  **Admin-only access** for managing employees and uploading images.
-  Add, update, delete, and fetch employee data.
-  Upload images tagged with YOLOv8 object detection results.
-  Query images by:
  - Employee ID
  - Tags
  - Employee ID + Tags
- ☁️ AWS Integration:
  - **DynamoDB** for storing metadata
  - **S3** for storing image files
- 🔍 Generate presigned URLs for secure image access and download.
- 🌐 Clean UI built with React.js to interact with the system.

---

## 🧰 Tech Stack

### ⚙️ Backend

- **FastAPI** – Web framework for high-performance APIs
- **Boto3** – AWS SDK for Python (S3, DynamoDB operations)
- **ultralytics YOLOv8** – For object detection and auto-tagging uploaded images
- **Pydantic** – For request validation
- **Pytest** – For unit testing API endpoints , bussiness logic function , pydantic model
- **CORS Middleware** – To allow frontend-backend interaction

### 🌐 Frontend

- **React.js** – Modern UI library
- **Axios** – Axios is a JavaScript library used to make HTTP requests from the browser (frontend) to a server (FastAPI backend).
- **CSS**  –  styling the UI rendered by reactjs component  

### ☁️ AWS Services

- **Amazon S3** – Image file storage as link of image 
- **Amazon DynamoDB** – NoSQL database for employee and image metadata

---

## 🛠️ Project Structure
```DRMS-project/
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── API/
│ │ │ └── employee.py
│ │ │ └── image.py
│ │ ├── Models/
│ │ │  └── employee.py
│ │ │  └── images.py
│ │ └── services/
│ │ ├── dynamodb_service.py
│ │ ├── dynamodb_service_image.py
│ │ └── s3_service.py
│ │ └── yolo_service.py
│ ├── tests/
│ │ └── api_test/
│ │ └── models_test.py
│ │ └── api_test/
│ │ └── services_test/
│ │ └── test_main.py
├── frontend/
│ └── src/
│ ├── components/
│ │ ├── EmployeeForm.js
│ │ ├── ScrollButton.js
│ │ └── QueryImages.js
│ ├── styles/
│ │ ├── EmployeeForm.css
│ │ ├── ScrollButton.css
│ │ └── QueryImages.css
│ ├── api/
│ │ └── apiService.js
│ ├── App.js
│ └── index.js
│ ├── App.css
│ └── index.css
```
---

## 🧪 Running the Project

### 1. Clone the Repo

git clone https://github.com/your-username/DRMS-project.git

cd DRMS-project


## Setup Backend

```
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

# Run FastAPI server
``uvicorn app.main:app --reload``

## Setup Frontend
```
cd frontend
npm install
npm start
```
##  Running Tests
``pytest -s tests``

`
