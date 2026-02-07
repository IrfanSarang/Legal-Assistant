from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
from typing import Optional

#--------Appointment Schemas-------
class AppointmentBase(BaseModel):
    client_id: int =Field(..., gt=0)
    date: datetime 
    description: Optional[str] = Field(None, max_length=500)

    @field_validator("date")
    def validate_future_date(cls, value):
        if value and value < datetime.now(timezone.utc):
           raise ValueError("Appointment date must be in the future")
        return value

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, max_length=500) 
    @field_validator("date")
    def validate_future_date(cls, value: Optional[datetime]):
        if value and value < datetime.now():
            raise ValueError("Appointment date must be in the future")
        return value   

class AppointmentResponse(BaseModel):
    id: int
    client_id: int
    date: datetime
    description: str

    model_config = {
    "from_attributes": True
}
