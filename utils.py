"""
Utility functions for the Faculty Monitoring System
"""

import os
import json
import logging
from datetime import datetime
import cv2
import numpy as np
import platform
import psutil
import re
import shutil
import glob

class Utils:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "data/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"faculty_monitoring_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def log_info(self, message):
        """Log info message"""
        self.logger.info(message)
        
    def log_error(self, message):
        """Log error message"""
        self.logger.error(message)
        
    def log_warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
        
    def get_system_info(self):
        """Get system information"""
        try:
            info = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'timestamp': datetime.now().isoformat()
            }
            return info
            
        except Exception as e:
            self.log_error(f"Error getting system info: {e}")
            return {}
            
    def create_directory(self, path):
        """Create directory if it doesn't exist"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
            
        except Exception as e:
            self.log_error(f"Error creating directory {path}: {e}")
            return False
            
    def save_json(self, data, file_path):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
            
        except Exception as e:
            self.log_error(f"Error saving JSON to {file_path}: {e}")
            return False
            
    def load_json(self, file_path):
        """Load data from JSON file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
            
        except Exception as e:
            self.log_error(f"Error loading JSON from {file_path}: {e}")
            return None
            
    def get_available_cameras(self):
        """Get list of available cameras"""
        available_cameras = []
        
        for i in range(10):  # Check first 10 camera indices
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        available_cameras.append(i)
                cap.release()
            except:
                pass
                
        return available_cameras
        
    def format_timestamp(self, timestamp=None):
        """Format timestamp for display"""
        if timestamp is None:
            timestamp = datetime.now()
        elif isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
            
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
    def calculate_file_size(self, file_path):
        """Calculate file size in human readable format"""
        try:
            size = os.path.getsize(file_path)
            
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
                
            return f"{size:.1f} TB"
            
        except Exception as e:
            self.log_error(f"Error calculating file size for {file_path}: {e}")
            return "Unknown"
            
    def cleanup_old_files(self, directory, days=7, extensions=None):
        """Clean up old files in directory"""
        try:
            from datetime import timedelta
            
            if not os.path.exists(directory):
                return 0
                
            cutoff_date = datetime.now() - timedelta(days=days)
            removed_count = 0
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                if os.path.isfile(file_path):
                    # Check extension if specified
                    if extensions and not any(filename.lower().endswith(ext) for ext in extensions):
                        continue
                        
                    # Check file age
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        removed_count += 1
                        self.log_info(f"Removed old file: {filename}")
                        
            return removed_count
            
        except Exception as e:
            self.log_error(f"Error cleaning up old files in {directory}: {e}")
            return 0
            
    def validate_email(self, email):
        """Validate email address format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def generate_report(self, data, report_type="summary"):
        """Generate system report"""
        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'report_type': report_type,
                'data': data
            }
            
            return report
            
        except Exception as e:
            self.log_error(f"Error generating report: {e}")
            return None

# Initialize logger
utils = Utils()
logger = utils.logger
