import cv2
import numpy as np
import os
import json
from datetime import datetime
import threading
import time
from ultralytics import YOLO
import face_recognition

class MLProcessor:
    def __init__(self):
        self.yolo_model = None
        self.reference_encodings = {}
        self.reference_names = []
        self.processing = False
        self.processing_thread = None
        
        # Detection settings
        self.confidence_threshold = 0.8
        self.nms_threshold = 0.4
        self.face_detection_model = 'yolov8n-face.pt'  # YOLOv8 face detection model
        
        # Initialize models
        self.initialize_models()
        self.load_reference_images()
        
    def initialize_models(self):
        """Initialize ML models"""
        try:
            print("Initializing ML models...")
            
            # Initialize YOLOv8 for face detection
            try:
                self.yolo_model = YOLO(self.face_detection_model)
                print("YOLOv8 face detection model loaded successfully")
            except Exception as e:
                print(f"Failed to load YOLOv8 model: {e}")
                print("Falling back to OpenCV Haar Cascade...")
                
                # Fallback to OpenCV Haar Cascade
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                
                if self.face_cascade.empty():
                    raise Exception("Failed to load Haar Cascade")
                    
                print("OpenCV Haar Cascade loaded as fallback")
                
        except Exception as e:
            print(f"Error initializing ML models: {e}")
            
    def load_reference_images(self):
        """Load reference images for faculty members"""
        reference_dir = "reference_images"
        
        if not os.path.exists(reference_dir):
            os.makedirs(reference_dir)
            print(f"Created reference images directory: {reference_dir}")
            return
            
        print("Loading reference images...")
        
        for filename in os.listdir(reference_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                faculty_name = os.path.splitext(filename)[0]
                image_path = os.path.join(reference_dir, filename)
                
                try:
                    # Load and process reference image
                    image = cv2.imread(image_path)
                    if image is not None:
                        # Convert BGR to RGB for face_recognition
                        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Get face encodings
                        face_encodings = face_recognition.face_encodings(rgb_image)
                        
                        if len(face_encodings) > 0:
                            # Use the first face found
                            self.reference_encodings[faculty_name] = face_encodings[0]
                            self.reference_names.append(faculty_name)
                            print(f"Loaded reference image for {faculty_name}")
                        else:
                            print(f"No face found in reference image for {faculty_name}")
                            
                except Exception as e:
                    print(f"Error loading reference image for {faculty_name}: {e}")
                    
        print(f"Loaded {len(self.reference_encodings)} reference images")
        
    def process_reference_image(self, faculty_name, image_path):
        """Process and save reference image for faculty member"""
        try:
            print(f"Processing reference image for {faculty_name}")
            
            # Create reference images directory
            reference_dir = "reference_images"
            os.makedirs(reference_dir, exist_ok=True)
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_path}")
                return False
                
            # Convert to RGB for face_recognition
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(rgb_image)
            
            if len(face_encodings) == 0:
                print(f"No face found in image for {faculty_name}")
                return False
                
            # Use the first face found
            face_encoding = face_encodings[0]
            
            # Save processed image
            output_path = os.path.join(reference_dir, f"{faculty_name}.jpg")
            cv2.imwrite(output_path, image)
            
            # Store encoding
            self.reference_encodings[faculty_name] = face_encoding
            if faculty_name not in self.reference_names:
                self.reference_names.append(faculty_name)
                
            # Save encoding to file for persistence
            encoding_file = os.path.join(reference_dir, f"{faculty_name}_encoding.npy")
            np.save(encoding_file, face_encoding)
            
            print(f"Reference image processed successfully for {faculty_name}")
            return True
            
        except Exception as e:
            print(f"Error processing reference image for {faculty_name}: {e}")
            return False
            
    def detect_faces_yolo(self, frame):
        """Detect faces using YOLOv8"""
        try:
            if self.yolo_model is None:
                return []
                
            # Run inference
            results = self.yolo_model(frame, conf=self.confidence_threshold, iou=self.nms_threshold)
            
            detected_faces = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        
                        # Convert to integers
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        # Extract face region
                        face_region = frame[y1:y2, x1:x2]
                        
                        detected_faces.append({
                            'bbox': (x1, y1, x2-x1, y2-y1),  # (x, y, width, height)
                            'confidence': float(confidence),
                            'face_region': face_region
                        })
                        
            return detected_faces
            
        except Exception as e:
            print(f"Error in YOLOv8 face detection: {e}")
            return []
            
    def detect_faces_opencv(self, frame):
        """Detect faces using OpenCV Haar Cascade (fallback)"""
        try:
            if not hasattr(self, 'face_cascade'):
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
                # Extract face region
                face_region = frame[y:y+h, x:x+w]
                
                detected_faces.append({
                    'bbox': (x, y, w, h),
                    'confidence': 0.9,  # Haar cascade doesn't provide confidence
                    'face_region': face_region
                })
                
            return detected_faces
            
        except Exception as e:
            print(f"Error in OpenCV face detection: {e}")
            return []
            
    def recognize_faces(self, frame, face_locations):
        """Recognize faces using face_recognition library"""
        try:
            if len(self.reference_encodings) == 0:
                return []
                
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert face locations to face_recognition format
            face_locations_rgb = []
            for (x, y, w, h) in face_locations:
                # Convert (x, y, w, h) to (top, right, bottom, left)
                top, right, bottom, left = y, x + w, y + h, x
                face_locations_rgb.append((top, right, bottom, left))
                
            # Get face encodings for detected faces
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations_rgb)
            
            recognized_faces = []
            
            for i, face_encoding in enumerate(face_encodings):
                # Compare with reference encodings
                matches = face_recognition.compare_faces(
                    list(self.reference_encodings.values()),
                    face_encoding,
                    tolerance=0.6
                )
                
                name = "Unknown"
                confidence = 0.0
                
                # Calculate face distances
                face_distances = face_recognition.face_distance(
                    list(self.reference_encodings.values()),
                    face_encoding
                )
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = self.reference_names[best_match_index]
                        # Convert distance to confidence (lower distance = higher confidence)
                        confidence = 1.0 - face_distances[best_match_index]
                        
                recognized_faces.append({
                    'name': name,
                    'confidence': confidence,
                    'bbox': face_locations[i]
                })
                
            return recognized_faces
            
        except Exception as e:
            print(f"Error in face recognition: {e}")
            return []
            
    def process_frame(self, frame):
        """Process a frame and return detections"""
        try:
            if frame is None:
                return []
                
            # Detect faces
            if self.yolo_model is not None:
                detected_faces = self.detect_faces_yolo(frame)
            else:
                detected_faces = self.detect_faces_opencv(frame)
                
            if len(detected_faces) == 0:
                return []
                
            # Extract face locations for recognition
            face_locations = [face['bbox'] for face in detected_faces]
            
            # Recognize faces
            recognized_faces = self.recognize_faces(frame, face_locations)
            
            # Combine detection and recognition results
            results = []
            for i, detection in enumerate(detected_faces):
                if i < len(recognized_faces):
                    recognition = recognized_faces[i]
                    result = {
                        'name': recognition['name'],
                        'confidence': recognition['confidence'],
                        'bbox': detection['bbox'],
                        'detection_confidence': detection['confidence']
                    }
                else:
                    result = {
                        'name': 'Unknown',
                        'confidence': 0.0,
                        'bbox': detection['bbox'],
                        'detection_confidence': detection['confidence']
                    }
                    
                results.append(result)
                
            return results
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return []
            
    def draw_detections(self, frame, detections):
        """Draw detection results on frame"""
        try:
            for detection in detections:
                bbox = detection['bbox']
                name = detection['name']
                confidence = detection['confidence']
                
                x, y, w, h = bbox
                
                # Choose color based on recognition
                if name == 'Unknown':
                    color = (0, 0, 255)  # Red for unknown
                else:
                    color = (0, 255, 0)  # Green for known
                    
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                # Draw label
                label = f"{name} ({confidence:.2f})"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                
                # Draw label background
                cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                            (x + label_size[0], y), color, -1)
                
                # Draw label text
                cv2.putText(frame, label, (x, y - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                          
            return frame
            
        except Exception as e:
            print(f"Error drawing detections: {e}")
            return frame
            
    def start_processing(self):
        """Start ML processing"""
        if not self.processing:
            self.processing = True
            print("ML processing started")
            
    def stop_processing(self):
        """Stop ML processing"""
        if self.processing:
            self.processing = False
            print("ML processing stopped")
            
    def update_settings(self, settings):
        """Update ML processing settings"""
        try:
            self.confidence_threshold = settings.get('confidence_threshold', 0.8)
            self.nms_threshold = settings.get('nms_threshold', 0.4)
            
            print(f"ML settings updated - Confidence: {self.confidence_threshold}, NMS: {self.nms_threshold}")
            
        except Exception as e:
            print(f"Error updating ML settings: {e}")
            
    def get_model_info(self):
        """Get information about loaded models"""
        info = {
            'face_detection': 'YOLOv8' if self.yolo_model else 'OpenCV Haar Cascade',
            'face_recognition': 'face_recognition library',
            'reference_images': len(self.reference_encodings),
            'confidence_threshold': self.confidence_threshold,
            'nms_threshold': self.nms_threshold
        }
        return info
        
    def get_reference_names(self):
        """Get list of reference names"""
        return self.reference_names.copy()
        
    def remove_reference_image(self, faculty_name):
        """Remove reference image for faculty member"""
        try:
            if faculty_name in self.reference_encodings:
                del self.reference_encodings[faculty_name]
                
            if faculty_name in self.reference_names:
                self.reference_names.remove(faculty_name)
                
            # Remove files
            reference_dir = "reference_images"
            image_file = os.path.join(reference_dir, f"{faculty_name}.jpg")
            encoding_file = os.path.join(reference_dir, f"{faculty_name}_encoding.npy")
            
            if os.path.exists(image_file):
                os.remove(image_file)
                
            if os.path.exists(encoding_file):
                os.remove(encoding_file)
                
            print(f"Reference image removed for {faculty_name}")
            return True
            
        except Exception as e:
            print(f"Error removing reference image for {faculty_name}: {e}")
            return False
