from sqlalchemy import Column, Integer, String
from app.database.client_db import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    phone = Column(String)
    email = Column(String, unique = True, index = True)