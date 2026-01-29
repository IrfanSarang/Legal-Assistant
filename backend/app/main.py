from fastapi import FastAPI
from app.api.client import router as client_router
from app.api.appointment import router as appointment_router




def create_app() -> FastAPI:
    app = FastAPI(
        title="Leagal Assistant Backend",
        description="Backend Service for Leagal Assistant Application",
        version="1.0.0"
    )

    #Register routers
    app.include_router(client_router, prefix="/api")
    app.include_router(appointment_router, prefix="/api")   
    

    return app

app = create_app()