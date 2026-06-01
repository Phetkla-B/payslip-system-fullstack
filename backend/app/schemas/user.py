from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    # Allow Paydantic to read data from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: str
    citizen_id: str
    role: str