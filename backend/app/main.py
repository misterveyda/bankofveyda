"""Main FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import Base, engine, SessionLocal
from app.config import get_settings
from app.api.v1.router import router as v1_router
from app.models.user import User
from app.utils.security import hash_password

settings = get_settings()
logger = logging.getLogger(__name__)


def create_initial_user() -> None:
    """Seed a demo user for prototype testing."""
    db = SessionLocal()
    try:
        if not db.query(User).first():
            demo_user = User(
                username="demo",
                email="demo@example.com",
                hashed_password=hash_password("demo123"),
            )
            db.add(demo_user)
            db.commit()
            logger.info("Created prototype demo user: demo / demo123")
    finally:
        db.close()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    create_initial_user()
    
    # Initialize FastAPI app
    app = FastAPI(
        title="Bank of Veyda",
        description="Compliance Simulator - Temporary Financial Identities",
        version="0.1.0",
        debug=settings.debug,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "http://127.0.0.1:4200",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": "0.1.0",
            "database": "connected",
        }
    
    # Include API routers
    app.include_router(v1_router, prefix="/api/v1")
    
    logger.info("FastAPI application initialized")
    return app


# Create app instance
app = create_app()
