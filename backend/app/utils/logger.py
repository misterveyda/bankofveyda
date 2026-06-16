"""Logging configuration."""

import logging
import sys
from typing import Optional

from app.config import get_settings

settings = get_settings()


def setup_logging(name: str, level: Optional[str] = None) -> logging.Logger:
    """Setup logger with standard configuration."""
    log_level = level or settings.log_level
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
