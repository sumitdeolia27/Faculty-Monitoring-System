"""
Utility functions for the Faculty Monitoring System
"""

import os
import json
import logging
from datetime import datetime
import cv2
import numpy as np

def setup_logging(log_level=logging.INFO):
    """Setup logging configuration"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('data/logs'):
        os.makedirs('data/logs')
    
    # Setup file handler
    log_file = f'data/logs/faculty_monitoring_{datetime.now().strftime("%Y%m%d")}.log'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def load_json_file(file_path, default=None):
    """Load JSON file with error handling"""
    if default is None:
        default = {}
        
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    
    return default

def save_json_file(file_path, data):
    """Save data to JSON file with error handling"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def validate_image_file(file_path):
    """Validate if file is a valid image"""
    try:
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in valid_extensions:
            return False, "Invalid file extension"
        
        # Try to load image
        image = cv2.imread(file_path)
        if image is None:
            return False, "Cannot read image file"
        
        # Check image dimensions
        height, width = image.shape[:2]
        if height < 50 or width < 50:
            return False, "Image too small (minimum 50x50 pixels)"
        
        return True, "Valid image file"
        
    except Exception as e:
        return False, f"Error validating image: {e}"

def resize_image(image, max_width=800, max_height=600):
    """Resize image while maintaining aspect ratio"""
    try:
        height, width = image.shape[:2]
        
        # Calculate scaling factor
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            return resized
        
        return image
        
    except Exception as e:
        print(f"Error resizing image: {e}")
        return image

def format_timestamp(timestamp=None, format_str="%Y-%m-%d %H:%M:%S"):
    """Format timestamp to string"""
    if timestamp is None:
        timestamp = datetime.now()
    
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp)
        except:
            return timestamp
    
    return timestamp.strftime(format_str)

def calculate_time_difference(start_time, end_time=None):
    """Calculate time difference in hours"""
    if end_time is None:
        end_time = datetime.now()
    
    if isinstance(start_time, str):
        try:
            start_time = datetime.fromisoformat(start_time)
        except:
            return 0
    
    if isinstance(end_time, str):
        try:
            end_time = datetime.fromisoformat(end_time)
        except:
            end_time = datetime.now()
    
    diff = end_time - start_time
    return diff.total_seconds() / 3600  # Convert to hours

def create_backup(source_file, backup_dir="backups"):
    """Create backup of a file"""
    try:
        if not os.path.exists(source_file):
            return False
        
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(source_file)
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy file
        import shutil
        shutil.copy2(source_file, backup_path)
        
        print(f"Backup created: {backup_path}")
        return True
        
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def cleanup_old_files(directory, days_to_keep=30, file_pattern="*"):
    """Clean up old files in directory"""
    try:
        import glob
        from datetime import timedelta
        
        if not os.path.exists(directory):
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        pattern = os.path.join(directory, file_pattern)
        files = glob.glob(pattern)
        
        removed_count = 0
        for file_path in files:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_date:
                    os.remove(file_path)
                    removed_count += 1
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
        
        if removed_count > 0:
            print(f"Cleaned up {removed_count} old files from {directory}")
        
        return removed_count
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return 0

def get_system_info():
    """Get system information"""
    import platform
    import psutil
    
    try:
        info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
        }
        return info
    except Exception as e:
        print(f"Error getting system info: {e}")
        return {}

# Initialize logger
logger = setup_logging()
