import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings
DATABASE_URL = f"sqlite:///{BASE_DIR}/vibecheck.db"

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Application settings
APP_NAME = "VibeCheck Business"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True") == "True"
