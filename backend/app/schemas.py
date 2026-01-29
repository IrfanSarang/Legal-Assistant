from pydantic import BaseModel

#-------Client Schemas-------

class ClientBase(BaseModel):
    name: str
    phone: str
    email: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int 
    class config:
        orm_mode = True


#--------Appointment Schemas-------
class AppointmentBase(BaseModel):
    client_id: int
    date: str
    description: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    class Config:
        orm_mode = True