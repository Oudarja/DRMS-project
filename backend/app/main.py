from fastapi import FastAPI

from app.API import employee, image

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware for receiving fronted request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# In FastAPI, a router is a modular way to organize your API endpoints (routes)
# by grouping related functionality together. This helps keep your code clean and
#  manageable as your project grows. Infine , Router is used to just groupe related
#  endpoints in case of api creation or nothing else. 

app.include_router(employee.router, prefix="/employees", tags=["Employees"])
app.include_router(image.router, prefix="/images", tags=["Images"])

@app.get("/")
def root():
    return {"message": "DRMS API is running"}




# uvicorn app.main:app --reload
# That tells Python:
# “Hey, main.py is inside the app package.”
# So from .API import employee now works, because Python understands the full package hierarchy.
# When under package a lot of import has to be done then uvicorn should have to be run from parent package. 