from fastapi import FastAPI

from app.routes import auth, users, admin, payslips
from app.models import user, payslip, upload_history
from app.core.database import engine, Base
from app.core.logger import logger

# Create instance of FastAPI
app = FastAPI()

# Log application startup
logger.info("Starting Payslip API")

# Create database tables
@app.on_event("startup")
def startup():
    logger.info("Creating database tables")
    Base.metadata.create_all(bind=engine)

# Log database initialization
logger.info("Database tables initialized")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(payslips.router, prefix="/payslips", tags=["payslips"])

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "Payslip API is running"}
    