from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.appointment_db import Base

class Appointment(Base):
    __tablename__ = "appointements"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    date = Column(DateTime)
    description = Column(String)


