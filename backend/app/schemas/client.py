from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#-------Client Schemas-------

class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr]

class ClientResponse(ClientCreate):
    id: int

    model_config = {
    "from_attributes": True
}
