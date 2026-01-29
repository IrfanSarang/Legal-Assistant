from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.client_db import SessionLocal, engine, Base
from app.models.client_model import Client
from app.schemas import ClientCreate, Client as ClientSchema

# CREATE ROUTER
router = APIRouter()

# CREATE TABLES
Base.metadata.create_all(bind=engine)

# DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- CREATE ----------------
@router.post("/clients/", response_model=ClientSchema)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# ---------------- READ ALL ----------------
@router.get("/clients/", response_model=list[ClientSchema])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

# ---------------- READ ONE ----------------
@router.get("/clients/{client_id}", response_model=ClientSchema)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# ---------------- UPDATE ----------------
@router.put("/clients/{client_id}", response_model=ClientSchema)
def update_client(client_id: int, updated: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in updated.dict().items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

# ---------------- DELETE ----------------
@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return {"detail": "Client deleted"}
