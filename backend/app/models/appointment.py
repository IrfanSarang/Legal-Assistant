from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.sql import func


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

    client = relationship("Client", back_populates="appointments")
