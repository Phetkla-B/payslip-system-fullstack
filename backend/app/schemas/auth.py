from pydantic import BaseModel


class RegisterRequest(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: str
    citizen_id: str
    password: str

class LoginRequest(BaseModel):
    citizen_id: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str