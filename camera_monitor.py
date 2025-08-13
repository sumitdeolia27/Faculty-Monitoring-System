import cv2
import threading
import time
from datetime import datetime
import numpy as np

class CameraMonitor:
    def __init__(self):
        self.camera = None
        self.monitoring = False
        self.current_frame = None
        self.capture_thread = None
        self.frame_lock = threading.Lock()
        
        # Default camera settings
        self.camera_index = 0
        self.resolution = (640, 480)
        self.fps = 30
        
    def initialize_camera(self):
        """Initialize the camera"""
        try:
            # Release existing camera if any
            if self.camera is not None:
                self.camera.release()
                
            # Initialize new camera
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if not self.camera.isOpened():
                raise Exception(f"Cannot open camera {self.camera_index}")
                
            # Set camera properties
            width, height = self.resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Test camera by reading a frame
            ret, frame = self.camera.read()
            if not ret:
                raise Exception("Cannot read from camera")
                
            print(f"Camera initialized successfully - Resolution: {width}x{height}, FPS: {self.fps}")
            return True
            
        except Exception as e:
            print(f"Failed to initialize camera: {e}")
            if self.camera is not None:
                self.camera.release()
                self.camera = None
            return False
            
    def start_monitoring(self):
        """Start camera monitoring"""
        if not self.monitoring:
            if self.initialize_camera():
                self.monitoring = True
                
                # Start capture thread
                self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
                self.capture_thread.start()
                
                print("Camera monitoring started")
                return True
            else:
                print("Failed to start camera monitoring")
                return False
        return True
        
    def stop_monitoring(self):
        """Stop camera monitoring"""
        if self.monitoring:
            self.monitoring = False
            
            # Wait for capture thread to finish
            if self.capture_thread and self.capture_thread.is_alive():
                self.capture_thread.join(timeout=2.0)
                
            # Release camera
            if self.camera is not None:
                self.camera.release()
                self.camera = None
                
            # Clear current frame
            with self.frame_lock:
                self.current_frame = None
                
            print("Camera monitoring stopped")
            
    def capture_loop(self):
        """Main capture loop"""
        frame_interval = 1.0 / self.fps if self.fps > 0 else 1.0 / 30
        
        while self.monitoring and self.camera is not None:
            try:
                ret, frame = self.camera.read()
                
                if ret and frame is not None:
                    # Store frame thread-safely
                    with self.frame_lock:
                        self.current_frame = frame.copy()
                else:
                    print("Failed to read frame from camera")
                    
                time.sleep(frame_interval)
                
            except Exception as e:
                print(f"Error in capture loop: {e}")
                break
                
        print("Capture loop ended")
        
    def get_current_frame(self):
        """Get the current frame thread-safely"""
        with self.frame_lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
            return None
            
    def is_monitoring(self):
        """Check if monitoring is active"""
        return self.monitoring
        
    def get_camera_info(self):
        """Get camera information"""
        if self.camera is not None and self.camera.isOpened():
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.camera.get(cv2.CAP_PROP_FPS))
            
            return {
                'index': self.camera_index,
                'resolution': f"{width}x{height}",
                'fps': fps,
                'status': 'active'
            }
        else:
            return {
                'index': self.camera_index,
                'resolution': f"{self.resolution[0]}x{self.resolution[1]}",
                'fps': self.fps,
                'status': 'inactive'
            }
            
    def update_settings(self, settings):
        """Update camera settings"""
        try:
            self.camera_index = settings.get('index', 0)
            
            # Parse resolution
            resolution_str = settings.get('resolution', '640x480')
            width, height = map(int, resolution_str.split('x'))
            self.resolution = (width, height)
            
            self.fps = settings.get('fps', 30)
            
            # If monitoring is active, restart with new settings
            if self.monitoring:
                self.stop_monitoring()
                time.sleep(0.5)  # Small delay
                self.start_monitoring()
                
            print(f"Camera settings updated: Index={self.camera_index}, Resolution={self.resolution}, FPS={self.fps}")
            
        except Exception as e:
            print(f"Error updating camera settings: {e}")
            
    def save_frame(self, filename=None):
        """Save current frame to file"""
        frame = self.get_current_frame()
        if frame is not None:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"camera_frame_{timestamp}.jpg"
                
            cv2.imwrite(filename, frame)
            return filename
        return None
        
    def get_available_cameras(self):
        """Get list of available cameras"""
        available_cameras = []
        
        # Test camera indices 0-5
        for i in range(6):
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
        
    def test_camera(self, camera_index):
        """Test if a camera index works"""
        try:
            cap = cv2.VideoCapture(camera_index)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                return ret and frame is not None
            return False
        except:
            return False
