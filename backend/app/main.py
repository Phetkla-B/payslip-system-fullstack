from fastapi import FastAPI

from app.routes import auth

# Create instance of FastAPI
app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Create ednpoint for root
#@app.get("/")
# def read_root():
#    return {"message": "Payslip API is running"}
    