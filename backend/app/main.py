from fastapi import FastAPI

# Create instance of FastAPI
app = FastAPI()

# Create ednpoint for root
@app.get("/")
def read_root():
    return {"message": "Payslip API is running"}
    