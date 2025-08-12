"""
Configuration settings for the Faculty Monitoring System
"""

import os

# Application Settings
APP_NAME = "Faculty Presence Monitoring & Alert System"
APP_VERSION = "1.0.0"
DEBUG_MODE = True

# File Paths
DATA_DIR = "data"
REFERENCE_IMAGES_DIR = os.path.join(DATA_DIR, "reference_images")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
RECORDINGS_DIR = os.path.join(DATA_DIR, "recordings")

# Database Files
FACULTY_DATA_FILE = os.path.join(DATA_DIR, "faculty_data.json")
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
DETECTION_LOG_FILE = os.path.join(LOGS_DIR, "detections.json")

# ML Model Settings
DEFAULT_DETECTION_THRESHOLD = 0.8
DEFAULT_PROCESSING_INTERVAL = 100  # milliseconds
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']

# Camera Settings
DEFAULT_CAMERA_FPS = 30
DEFAULT_CAMERA_RESOLUTION = (640, 480)
MAX_CAMERAS = 10

# Alert Settings
DEFAULT_ALERT_THRESHOLD_HOURS = 2
DEFAULT_HIGH_PRIORITY_THRESHOLD_HOURS = 4
ALERT_CLEANUP_DAYS = 30

# Email Settings
DEFAULT_EMAIL_SERVER = "smtp.gmail.com"
DEFAULT_EMAIL_PORT = 587

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
THEME_COLORS = {
    'primary': '#3498db',
    'secondary': '#2c3e50',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#9b59b6',
    'light': '#ecf0f1',
    'dark': '#34495e'
}

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [DATA_DIR, REFERENCE_IMAGES_DIR, LOGS_DIR, RECORDINGS_DIR]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Initialize directories when module is imported
create_directories()
