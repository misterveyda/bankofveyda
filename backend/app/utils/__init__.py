"""Utility functions."""

from app.models import BurnerAccount
import random
import string


def generate_account_number() -> str:
    """Generate a random 17-digit account number."""
    return ''.join(random.choices(string.digits, k=17))


def generate_routing_number() -> str:
    """Generate a random 9-digit routing number (sandbox only)."""
    return ''.join(random.choices(string.digits, k=9))


def calculate_checksum(account_number: str) -> str:
    """Calculate checksum for account number validation."""
    # Simplified checksum calculation
    total = sum(int(digit) for digit in account_number)
    return str(total % 10)
