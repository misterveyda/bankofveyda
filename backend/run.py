#!/usr/bin/env python
"""Entry point for running the FastAPI application."""

import uvicorn
import logging
import sys

from app.config import get_settings

settings = get_settings()

# Setup logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run the application."""
    logger.info("Starting Bank of Veyda API Server...")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
