import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings
DATABASE_URL = f"sqlite:///{BASE_DIR}/vibecheck.db"

# Application settings
APP_NAME = "VibeCheck Business"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True") == "True"
