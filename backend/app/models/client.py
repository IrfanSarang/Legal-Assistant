from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    phone = Column(String(10))
    email = Column(String(255), unique=True, index=True)

    appointments = relationship(
    "Appointment",
    back_populates="client",
    cascade="all, delete-orphan"
)
