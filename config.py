import json
import os

class Config:
    def __init__(self):
        self.config_file = "data/config.json"
        self.default_config = {
            'camera': {
                'index': 0,
                'resolution': '640x480',
                'fps': 30
            },
            'detection': {
                'confidence_threshold': 0.8,
                'nms_threshold': 0.4,
                'face_detection_model': 'yolov8n-face.pt'
            },
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'email': '',
                'password': ''
            },
            'system': {
                'auto_start_monitoring': False,
                'save_screenshots': True,
                'log_level': 'INFO'
            }
        }
        
        self.config = self.default_config.copy()
        self.ensure_data_directory()
        self.load_config()
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    
                # Merge with default config to ensure all keys exist
                self.config = self.merge_configs(self.default_config, loaded_config)
                print("Configuration loaded successfully")
            else:
                # Save default config
                self.save_config()
                print("Default configuration created")
                
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self.config = self.default_config.copy()
            
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print("Configuration saved successfully")
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
            
    def merge_configs(self, default, loaded):
        """Merge loaded config with default config"""
        merged = default.copy()
        
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
                
        return merged
        
    def get_config(self, section=None):
        """Get configuration section or entire config"""
        if section:
            return self.config.get(section, {})
        return self.config.copy()
        
    def set_config(self, section, key, value):
        """Set configuration value"""
        try:
            if section not in self.config:
                self.config[section] = {}
                
            self.config[section][key] = value
            self.save_config()
            return True
            
        except Exception as e:
            print(f"Error setting configuration: {e}")
            return False
            
    def save_settings(self, settings):
        """Save all settings"""
        try:
            self.config.update(settings)
            self.save_config()
            return True
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
            
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        try:
            self.config = self.default_config.copy()
            self.save_config()
            print("Configuration reset to defaults")
            return True
            
        except Exception as e:
            print(f"Error resetting configuration: {e}")
            return False
