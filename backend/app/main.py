"""Main FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import Base, engine
from app.config import get_settings
from app.api.v1.router import router as v1_router

settings = get_settings()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
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
