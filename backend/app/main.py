from fastapi import FastAPI
from app.api.client import router as client_router
from app.api.appointment import router as appointment_router
from fastapi.middleware.cors import CORSMiddleware



def create_app() -> FastAPI:
    app = FastAPI(
        title="Leagal Assistant Backend",
        description="Backend Service for Leagal Assistant Application",
        version="1.0.0"
    )

 # ---------------- CORS ----------------
    origins = [
        "http://localhost:3000",  # Next.js frontend dev
        "http://192.168.0.102:3000",
        "http://127.0.0.1:3000",
        # Add production frontend URLs here
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,      # allow frontend URLs
        allow_credentials=True,     # allow cookies / auth headers
        allow_methods=["*"],        # allow GET, POST, PUT, DELETE
        allow_headers=["*"],        # allow all headers
    )

    # ---------------- Routers ----------------
    app.include_router(client_router, prefix="/api")
    app.include_router(appointment_router, prefix="/api")   

    return app

app = create_app()