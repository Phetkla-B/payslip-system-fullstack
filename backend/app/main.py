from fastapi import FastAPI

from app.routes import auth, users
from app.models import user
from app.core.database import engine, Base
from app.core.logger import logger

# Create instance of FastAPI
app = FastAPI()

# Log application startup
logger.info("Starting Payslip API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Log database initialization
logger.info("Database tables initialized")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "Payslip API is running"}
    