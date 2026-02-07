from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.schemas.appointment_expanded import AppointmentWithClientResponse

from sqlalchemy.orm import joinedload

# ✅ CREATE ROUTER
router = APIRouter()

# ✅ DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- CREATE ----------------
@router.post("/", response_model=AppointmentResponse)
def create_appointment(app: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = Appointment(**app.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

# ---------------- READ ALL ----------------
@router.get("/", response_model=list[AppointmentWithClientResponse])
def get_appointments_with_clients(db: Session = Depends(get_db)):
    return (
        db.query(Appointment)
        .options(joinedload(Appointment.client))
        .all()
    )

# ---------------- READ ONE ----------------
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# ---------------- UPDATE ----------------
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    updated: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)
    return appointment

# ---------------- DELETE ----------------
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted"}
