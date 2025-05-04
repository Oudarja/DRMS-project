from fastapi import FastAPI

from app.API import employee, image

app = FastAPI()

# Include routers
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