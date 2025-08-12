import cv2
import threading
import time
from datetime import datetime
import numpy as np

class CameraMonitor:
    def __init__(self):
        self.cameras = {}
        self.active_cameras = []
        self.monitoring = False
        self.capture_threads = {}
        
        # Initialize camera configurations
        self.camera_configs = {
            'Main Entrance': {'id': 0, 'fps': 30, 'resolution': (640, 480)},
            'Faculty Lounge': {'id': 1, 'fps': 25, 'resolution': (640, 480)},
            'Corridor A': {'id': 2, 'fps': 30, 'resolution': (640, 480)},
            'Conference Room': {'id': 3, 'fps': 30, 'resolution': (640, 480)},
            'Library': {'id': 4, 'fps': 0, 'resolution': (640, 480)},  # Inactive
            'Cafeteria': {'id': 5, 'fps': 20, 'resolution': (640, 480)}
        }
        
    def initialize_cameras(self):
        """Initialize all available cameras"""
        for camera_name, config in self.camera_configs.items():
            if config['fps'] > 0:  # Only initialize active cameras
                try:
                    # For demo purposes, we'll simulate camera initialization
                    # In real implementation, you would use cv2.VideoCapture(config['id'])
                    self.cameras[camera_name] = {
                        'capture': None,  # cv2.VideoCapture(config['id'])
                        'config': config,
                        'status': 'active',
                        'last_frame': None,
                        'frame_count': 0
                    }
                    self.active_cameras.append(camera_name)
                    print(f"Camera {camera_name} initialized successfully")
                except Exception as e:
                    print(f"Failed to initialize camera {camera_name}: {e}")
                    self.cameras[camera_name] = {
                        'capture': None,
                        'config': config,
                        'status': 'error',
                        'last_frame': None,
                        'frame_count': 0
                    }
                    
    def start_monitoring(self):
        """Start camera monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.initialize_cameras()
            
            # Start capture threads for each active camera
            for camera_name in self.active_cameras:
                thread = threading.Thread(
                    target=self.capture_loop, 
                    args=(camera_name,), 
                    daemon=True
                )
                thread.start()
                self.capture_threads[camera_name] = thread
                
            print("Camera monitoring started")
            
    def stop_monitoring(self):
        """Stop camera monitoring"""
        self.monitoring = False
        
        # Release all cameras
        for camera_name, camera_data in self.cameras.items():
            if camera_data['capture']:
                camera_data['capture'].release()
                
        self.cameras.clear()
        self.active_cameras.clear()
        self.capture_threads.clear()
        
        print("Camera monitoring stopped")
        
    def capture_loop(self, camera_name):
        """Main capture loop for a camera"""
        camera_data = self.cameras[camera_name]
        fps = camera_data['config']['fps']
        frame_interval = 1.0 / fps if fps > 0 else 1.0
        
        while self.monitoring and camera_name in self.cameras:
            try:
                # Simulate frame capture
                # In real implementation, you would use:
                # ret, frame = camera_data['capture'].read()
                
                # For demo, create a dummy frame
                frame = self.create_dummy_frame(camera_data['config']['resolution'])
                
                if frame is not None:
                    camera_data['last_frame'] = frame
                    camera_data['frame_count'] += 1
                    camera_data['last_update'] = datetime.now()
                    
                    # Yield frame for processing
                    yield frame
                    
                time.sleep(frame_interval)
                
            except Exception as e:
                print(f"Error in capture loop for {camera_name}: {e}")
                camera_data['status'] = 'error'
                break
                
    def create_dummy_frame(self, resolution):
        """Create a dummy frame for demonstration"""
        width, height = resolution
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add some visual elements
        cv2.rectangle(frame, (50, 50), (width-50, height-50), (100, 100, 100), 2)
        cv2.putText(frame, f"Camera Feed", (width//4, height//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, datetime.now().strftime("%H:%M:%S"), 
                   (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
        
    def get_latest_frame(self, camera_name):
        """Get the latest frame from a camera"""
        if camera_name in self.cameras:
            return self.cameras[camera_name]['last_frame']
        return None
        
    def get_camera_status(self, camera_name):
        """Get status of a specific camera"""
        if camera_name in self.cameras:
            return self.cameras[camera_name]['status']
        return 'inactive'
        
    def get_all_camera_status(self):
        """Get status of all cameras"""
        status = {}
        for camera_name, config in self.camera_configs.items():
            if camera_name in self.cameras:
                status[camera_name] = {
                    'status': self.cameras[camera_name]['status'],
                    'fps': config['fps'],
                    'frame_count': self.cameras[camera_name]['frame_count']
                }
            else:
                status[camera_name] = {
                    'status': 'inactive',
                    'fps': 0,
                    'frame_count': 0
                }
        return status
        
    def set_camera_fps(self, camera_name, fps):
        """Set FPS for a specific camera"""
        if camera_name in self.camera_configs:
            self.camera_configs[camera_name]['fps'] = fps
            
            # If camera is active, restart it with new settings
            if camera_name in self.cameras and self.monitoring:
                self.restart_camera(camera_name)
                
    def restart_camera(self, camera_name):
        """Restart a specific camera"""
        if camera_name in self.cameras:
            # Stop current capture
            if self.cameras[camera_name]['capture']:
                self.cameras[camera_name]['capture'].release()
                
            # Reinitialize
            try:
                config = self.camera_configs[camera_name]
                # self.cameras[camera_name]['capture'] = cv2.VideoCapture(config['id'])
                self.cameras[camera_name]['status'] = 'active'
                print(f"Camera {camera_name} restarted")
            except Exception as e:
                print(f"Failed to restart camera {camera_name}: {e}")
                self.cameras[camera_name]['status'] = 'error'
                
    def save_frame(self, camera_name, filename=None):
        """Save current frame from camera"""
        if camera_name in self.cameras:
            frame = self.cameras[camera_name]['last_frame']
            if frame is not None:
                if filename is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{camera_name}_{timestamp}.jpg"
                    
                cv2.imwrite(filename, frame)
                return filename
        return None
