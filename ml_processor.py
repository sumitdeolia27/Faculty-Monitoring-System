import cv2
import numpy as np
import os
import json
from datetime import datetime
import random

class MLProcessor:
    def __init__(self):
        self.face_cascade = None
        self.reference_images = {}
        self.detection_threshold = 0.8
        self.processing_interval = 100  # ms
        
        # Initialize face detection
        self.initialize_models()
        self.load_reference_images()
        
    def initialize_models(self):
        """Initialize ML models"""
        try:
            # Initialize OpenCV face cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            print("Face detection model initialized (OpenCV Haar Cascade)")
            
            # In a real implementation, you would also initialize:
            # - YOLOv8 model for face detection
            # - DeepFace for face verification
            # - TensorFlow/PyTorch models
            
        except Exception as e:
            print(f"Error initializing ML models: {e}")
            
    def load_reference_images(self):
        """Load reference images for faculty members"""
        reference_dir = "reference_images"
        if os.path.exists(reference_dir):
            for filename in os.listdir(reference_dir):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    faculty_name = os.path.splitext(filename)[0]
                    image_path = os.path.join(reference_dir, filename)
                    
                    try:
                        # Load and process reference image
                        image = cv2.imread(image_path)
                        if image is not None:
                            # Extract face features (simplified)
                            features = self.extract_face_features(image)
                            if features is not None:
                                self.reference_images[faculty_name] = {
                                    'features': features,
                                    'image_path': image_path,
                                    'processed_at': datetime.now().isoformat()
                                }
                                print(f"Loaded reference image for {faculty_name}")
                    except Exception as e:
                        print(f"Error loading reference image for {faculty_name}: {e}")
                        
    def extract_face_features(self, image):
        """Extract face features from image"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Get the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                
                # Extract face region
                face_roi = gray[y:y+h, x:x+w]
                
                # Resize to standard size
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # In a real implementation, you would use deep learning features
                # For demo, we'll use histogram as a simple feature
                features = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
                return features.flatten()
                
        except Exception as e:
            print(f"Error extracting face features: {e}")
            
        return None
        
    def process_reference_image(self, faculty_name, image_path):
        """Process and save reference image for faculty member"""
        try:
            # Create reference images directory
            reference_dir = "reference_images"
            os.makedirs(reference_dir, exist_ok=True)
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return False
                
            # Extract features
            features = self.extract_face_features(image)
            if features is None:
                return False
                
            # Save processed image
            output_path = os.path.join(reference_dir, f"{faculty_name}.jpg")
            cv2.imwrite(output_path, image)
            
            # Store features
            self.reference_images[faculty_name] = {
                'features': features,
                'image_path': output_path,
                'processed_at': datetime.now().isoformat()
            }
            
            # Save features to file
            features_file = os.path.join(reference_dir, f"{faculty_name}_features.json")
            with open(features_file, 'w') as f:
                json.dump({
                    'features': features.tolist(),
                    'processed_at': datetime.now().isoformat()
                }, f)
                
            print(f"Reference image processed for {faculty_name}")
            return True
            
        except Exception as e:
            print(f"Error processing reference image: {e}")
            return False
            
    def detect_faces_in_frame(self, frame):
        """Detect faces in a frame"""
        try:
            if self.face_cascade is None:
                return []
                
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            detected_faces = []
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # Extract features
                features = cv2.calcHist([face_roi], [0], None, [256], [0, 256]).flatten()
                
                detected_faces.append({
                    'bbox': (x, y, w, h),
                    'features': features,
                    'roi': face_roi
                })
                
            return detected_faces
            
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
            
    def verify_face(self, detected_features):
        """Verify detected face against reference images"""
        best_match = None
        best_confidence = 0
        
        for faculty_name, reference_data in self.reference_images.items():
            try:
                reference_features = reference_data['features']
                
                # Calculate similarity (simplified correlation)
                correlation = cv2.compareHist(
                    detected_features.astype(np.float32),
                    reference_features.astype(np.float32),
                    cv2.HISTCMP_CORREL
                )
                
                if correlation > best_confidence and correlation > self.detection_threshold:
                    best_confidence = correlation
                    best_match = faculty_name
                    
            except Exception as e:
                print(f"Error comparing with {faculty_name}: {e}")
                
        return best_match, best_confidence
        
    def process_frame(self):
        """Process a frame and return detections"""
        # Simulate frame processing
        detections = []
        
        # Simulate random detections for demo
        faculty_names = list(self.reference_images.keys()) + ["Unknown Person"]
        cameras = ["Main Entrance", "Faculty Lounge", "Corridor A", "Conference Room", "Cafeteria"]
        
        # Generate 0-2 random detections
        num_detections = random.randint(0, 2)
        
        for _ in range(num_detections):
            detection = {
                'name': random.choice(faculty_names),
                'confidence': random.uniform(0.6, 0.98),
                'camera': random.choice(cameras),
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'bbox': (
                    random.randint(50, 200),
                    random.randint(50, 150),
                    random.randint(80, 120),
                    random.randint(80, 120)
                )
            }
            detections.append(detection)
            
        return detections
        
    def process_camera_frame(self, frame, camera_name):
        """Process frame from specific camera"""
        try:
            # Detect faces
            detected_faces = self.detect_faces_in_frame(frame)
            
            detections = []
            for face_data in detected_faces:
                # Verify face
                faculty_name, confidence = self.verify_face(face_data['features'])
                
                if faculty_name:
                    detection = {
                        'name': faculty_name,
                        'confidence': confidence,
                        'camera': camera_name,
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'bbox': face_data['bbox']
                    }
                else:
                    detection = {
                        'name': 'Unknown Person',
                        'confidence': 0.5,
                        'camera': camera_name,
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'bbox': face_data['bbox']
                    }
                    
                detections.append(detection)
                
            return detections
            
        except Exception as e:
            print(f"Error processing frame from {camera_name}: {e}")
            return []
            
    def set_detection_threshold(self, threshold):
        """Set detection confidence threshold"""
        self.detection_threshold = max(0.1, min(1.0, threshold))
        
    def get_model_info(self):
        """Get information about loaded models"""
        return {
            'face_detection': 'OpenCV Haar Cascade' if self.face_cascade else 'Not loaded',
            'face_verification': 'Histogram Correlation (Demo)',
            'reference_images': len(self.reference_images),
            'detection_threshold': self.detection_threshold
        }
        
    def update_model_settings(self, settings):
        """Update ML model settings"""
        if 'detection_threshold' in settings:
            self.set_detection_threshold(settings['detection_threshold'])
            
        if 'processing_interval' in settings:
            self.processing_interval = settings['processing_interval']
            
        print(f"ML settings updated: {settings}")
