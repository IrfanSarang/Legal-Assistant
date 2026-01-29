from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.appointment_db import SessionLocal, engine, Base
from app.models.appointment_model import Appointment
from app.schemas import AppointmentCreate, Appointment as AppointmentSchema

# ✅ CREATE ROUTER
router = APIRouter()

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- CREATE ----------------
@router.post("/appointments/", response_model=AppointmentSchema)
def create_appointment(app: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = Appointment(**app.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

# ---------------- READ ALL ----------------
@router.get("/appointments/", response_model=list[AppointmentSchema])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

# ---------------- READ ONE ----------------
@router.get("/appointments/{appointment_id}", response_model=AppointmentSchema)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# ---------------- UPDATE ----------------
@router.put("/appointments/{appointment_id}", response_model=AppointmentSchema)
def update_appointment(
    appointment_id: int,
    updated: AppointmentCreate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in updated.dict().items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)
    return appointment

# ---------------- DELETE ----------------
@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted"}
