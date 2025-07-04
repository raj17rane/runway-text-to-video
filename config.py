import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
API_BASE_URL = "https://api.runwayml.com/v1"

# Default Settings
DEFAULT_RESOLUTION = os.getenv("DEFAULT_RESOLUTION", "1280x768")
DEFAULT_DURATION = int(os.getenv("DEFAULT_DURATION", "4"))
DEFAULT_MOTION_STRENGTH = float(os.getenv("DEFAULT_MOTION_STRENGTH", "0.8"))

# App Configuration
MAX_WAIT_TIME = int(os.getenv("MAX_WAIT_TIME", "300"))  # seconds
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Video Settings
SUPPORTED_RESOLUTIONS = [
    "1280x768",    # HD Landscape
    "1920x1080",   # Full HD Landscape
    "768x1280",    # HD Portrait
    "1080x1920"    # Full HD Portrait
]

DURATION_LIMITS = {
    "min": 1,
    "max": 10
}

MOTION_STRENGTH_LIMITS = {
    "min": 0.0,
    "max": 1.0
}

# API Endpoints
ENDPOINTS = {
    "generate": f"{API_BASE_URL}/generate",
    "tasks": f"{API_BASE_URL}/tasks"
}

# File Settings
OUTPUT_DIR = "generated_videos"
ALLOWED_EXTENSIONS = [".mp4", ".mov", ".avi"]

# Validation
def validate_config():
    """Validate configuration settings"""
    if not RUNWAY_API_KEY:
        raise ValueError("RUNWAY_API_KEY is required")
    
    if DEFAULT_RESOLUTION not in SUPPORTED_RESOLUTIONS:
        raise ValueError(f"Invalid resolution: {DEFAULT_RESOLUTION}")
    
    if not (DURATION_LIMITS["min"] <= DEFAULT_DURATION <= DURATION_LIMITS["max"]):
        raise ValueError(f"Invalid duration: {DEFAULT_DURATION}")
    
    if not (MOTION_STRENGTH_LIMITS["min"] <= DEFAULT_MOTION_STRENGTH <= MOTION_STRENGTH_LIMITS["max"]):
        raise ValueError(f"Invalid motion strength: {DEFAULT_MOTION_STRENGTH}")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)