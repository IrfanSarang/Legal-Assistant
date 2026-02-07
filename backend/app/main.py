from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.database import Base
from app.core.database import engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="Leagal Assistant Backend",
        description="Backend Service for Leagal Assistant Application",
        version="1.0.0"
    )

 # ---------------- CORS ----------------
    origins = [
        "http://localhost:3000",  
        "http://192.168.0.101:3000",
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


    # CREATE TABLES
    Base.metadata.create_all(bind=engine)

  # ----------- API Router -----------
    app.include_router(api_router)  

    return app

app = create_app()