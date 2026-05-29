from fastapi import FastAPI

from app.routes import auth, users
from app.models import user
from app.core.database import engine, Base

# Create instance of FastAPI
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Create ednpoint for root
#@app.get("/")
# def read_root():
#    return {"message": "Payslip API is running"}
    