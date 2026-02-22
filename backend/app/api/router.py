from fastapi import APIRouter

from app.api.v1.client import router as client_router
from app.api.v1.appointment import router as appointment_router
from app.api.v1.legal import router as legal_router
from app.api.v1.contract import router as contract_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(
    client_router,
    prefix="/clients",
    tags=["Clients"]
)

api_router.include_router(
    appointment_router,
    prefix="/appointments",
    tags=["Appointments"]
)

api_router.include_router(
    legal_router,
    prefix="/legal",
    tags=["Legal Intelligence"]
)

api_router.include_router(
    contract_router,
    prefix="/contract",
    tags=["Contract "]
)