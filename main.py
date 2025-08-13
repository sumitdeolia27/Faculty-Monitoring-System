import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import threading
import time
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
import numpy as np

from faculty_manager import FacultyManager
from camera_monitor import CameraMonitor
from ml_processor import MLProcessor
from alert_system import AlertSystem
from config import Config
from utils import Utils

class FacultyMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Faculty Presence Monitoring & Alert System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.config = Config()
        self.faculty_manager = FacultyManager()
        self.camera_monitor = CameraMonitor()
        self.ml_processor = MLProcessor()
        self.alert_system = AlertSystem()
        self.utils = Utils()
        
        # Initialize variables
        self.monitoring_active = False
        self.current_frame = None
        self.detection_log = []
        
        # Create GUI
        self.create_gui()
        
        # Start background processes
        self.start_background_processes()
        
    def create_gui(self):
        """Create the main GUI interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_faculty_tab()
        self.create_monitoring_tab()
        self.create_alerts_tab()
        self.create_settings_tab()
        
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_label = ttk.Label(dashboard_frame, text="Faculty Monitoring Dashboard", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(dashboard_frame, text="System Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create stats labels
        self.stats_labels = {}
        stats_data = [
            ("Total Faculty", "total_faculty"),
            ("Active Cameras", "active_cameras"),
            ("Detections Today", "detections_today"),
            ("System Status", "system_status")
        ]
        
        for i, (label_text, key) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            label = ttk.Label(stats_frame, text=f"{label_text}:")
            label.grid(row=row, column=col*2, sticky=tk.W, padx=10, pady=5)
            
            value_label = ttk.Label(stats_frame, text="0", font=('Arial', 10, 'bold'))
            value_label.grid(row=row, column=col*2+1, sticky=tk.W, padx=10, pady=5)
            
            self.stats_labels[key] = value_label
            
        # Recent activity frame
        activity_frame = ttk.LabelFrame(dashboard_frame, text="Recent Activity")
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Activity listbox with scrollbar
        activity_scroll_frame = ttk.Frame(activity_frame)
        activity_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.activity_listbox = tk.Listbox(activity_scroll_frame, height=15)
        activity_scrollbar = ttk.Scrollbar(activity_scroll_frame, orient=tk.VERTICAL, 
                                         command=self.activity_listbox.yview)
        self.activity_listbox.configure(yscrollcommand=activity_scrollbar.set)
        
        self.activity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        activity_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_faculty_tab(self):
        """Create faculty management tab"""
        faculty_frame = ttk.Frame(self.notebook)
        self.notebook.add(faculty_frame, text="Faculty Management")
        
        # Title
        title_label = ttk.Label(faculty_frame, text="Faculty Management", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Control frame
        control_frame = ttk.Frame(faculty_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        ttk.Button(control_frame, text="Add Faculty", 
                  command=self.add_faculty_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Edit Faculty", 
                  command=self.edit_faculty_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Delete Faculty", 
                  command=self.delete_faculty).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Upload Reference Image", 
                  command=self.upload_reference_image).pack(side=tk.LEFT, padx=5)
        
        # Faculty list frame
        list_frame = ttk.LabelFrame(faculty_frame, text="Faculty List")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for faculty list
        columns = ("ID", "Name", "Department", "Email", "Status", "Last Seen")
        self.faculty_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.faculty_tree.heading(col, text=col)
            self.faculty_tree.column(col, width=120)
            
        # Scrollbar for treeview
        faculty_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                        command=self.faculty_tree.yview)
        self.faculty_tree.configure(yscrollcommand=faculty_scrollbar.set)
        
        self.faculty_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        faculty_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_monitoring_tab(self):
        """Create live monitoring tab"""
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="Live Monitoring")
        
        # Title
        title_label = ttk.Label(monitoring_frame, text="Live Camera Monitoring", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Control frame
        control_frame = ttk.Frame(monitoring_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Monitoring controls
        self.start_button = ttk.Button(control_frame, text="Start Monitoring", 
                                     command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Monitoring", 
                                    command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Take Screenshot", 
                  command=self.take_screenshot).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.monitoring_status_label = ttk.Label(control_frame, text="Status: Stopped", 
                                               foreground="red")
        self.monitoring_status_label.pack(side=tk.RIGHT, padx=10)
        
        # Main monitoring frame
        main_monitor_frame = ttk.Frame(monitoring_frame)
        main_monitor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Camera feed frame
        camera_frame = ttk.LabelFrame(main_monitor_frame, text="Camera Feed")
        camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Camera display label
        self.camera_label = ttk.Label(camera_frame, text="Camera feed will appear here", 
                                    background="black", foreground="white")
        self.camera_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Detection log frame
        log_frame = ttk.LabelFrame(main_monitor_frame, text="Detection Log")
        log_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        log_frame.configure(width=300)
        
        # Detection log listbox
        self.detection_listbox = tk.Listbox(log_frame, width=40, height=20)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, 
                                    command=self.detection_listbox.yview)
        self.detection_listbox.configure(yscrollcommand=log_scrollbar.set)
        
        self.detection_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_alerts_tab(self):
        """Create alerts tab"""
        alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(alerts_frame, text="Alerts")
        
        # Title
        title_label = ttk.Label(alerts_frame, text="Alert Management", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Control frame
        control_frame = ttk.Frame(alerts_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="Clear All Alerts", 
                  command=self.clear_alerts).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export Alerts", 
                  command=self.export_alerts).pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        filter_frame = ttk.LabelFrame(alerts_frame, text="Filter Alerts")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Priority:").pack(side=tk.LEFT, padx=5)
        self.alert_filter_var = tk.StringVar(value="All")
        alert_filter_combo = ttk.Combobox(filter_frame, textvariable=self.alert_filter_var,
                                        values=["All", "High", "Medium", "Low"], state="readonly")
        alert_filter_combo.pack(side=tk.LEFT, padx=5)
        alert_filter_combo.bind("<<ComboboxSelected>>", self.filter_alerts)
        
        # Alerts list frame
        alerts_list_frame = ttk.LabelFrame(alerts_frame, text="Active Alerts")
        alerts_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Alerts treeview
        alert_columns = ("Time", "Type", "Priority", "Message", "Status")
        self.alerts_tree = ttk.Treeview(alerts_list_frame, columns=alert_columns, 
                                      show="headings", height=15)
        
        for col in alert_columns:
            self.alerts_tree.heading(col, text=col)
            self.alerts_tree.column(col, width=150)
            
        # Scrollbar for alerts
        alerts_scrollbar = ttk.Scrollbar(alerts_list_frame, orient=tk.VERTICAL, 
                                       command=self.alerts_tree.yview)
        self.alerts_tree.configure(yscrollcommand=alerts_scrollbar.set)
        
        self.alerts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        alerts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Title
        title_label = ttk.Label(settings_frame, text="System Settings", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Create notebook for settings categories
        settings_notebook = ttk.Notebook(settings_frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Camera settings
        camera_settings_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(camera_settings_frame, text="Camera")
        
        # Detection settings
        detection_settings_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(detection_settings_frame, text="Detection")
        
        # Alert settings
        alert_settings_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(alert_settings_frame, text="Alerts")
        
        # Create camera settings
        self.create_camera_settings(camera_settings_frame)
        self.create_detection_settings(detection_settings_frame)
        self.create_alert_settings(alert_settings_frame)
        
        # Save button
        ttk.Button(settings_frame, text="Save Settings", 
                  command=self.save_settings).pack(pady=10)
        
    def create_camera_settings(self, parent):
        """Create camera settings"""
        # Camera selection
        camera_frame = ttk.LabelFrame(parent, text="Camera Configuration")
        camera_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(camera_frame, text="Camera Index:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.camera_index_var = tk.StringVar(value="0")
        ttk.Entry(camera_frame, textvariable=self.camera_index_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(camera_frame, text="Resolution:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.resolution_var = tk.StringVar(value="640x480")
        resolution_combo = ttk.Combobox(camera_frame, textvariable=self.resolution_var,
                                      values=["640x480", "1280x720", "1920x1080"], state="readonly")
        resolution_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(camera_frame, text="FPS:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.fps_var = tk.StringVar(value="30")
        ttk.Entry(camera_frame, textvariable=self.fps_var, width=10).grid(row=2, column=1, padx=5, pady=5)
        
    def create_detection_settings(self, parent):
        """Create detection settings"""
        # YOLOv8 settings
        yolo_frame = ttk.LabelFrame(parent, text="YOLOv8 Configuration")
        yolo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(yolo_frame, text="Confidence Threshold:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.confidence_var = tk.DoubleVar(value=0.8)
        confidence_scale = ttk.Scale(yolo_frame, from_=0.1, to=1.0, variable=self.confidence_var, 
                                   orient=tk.HORIZONTAL, length=200)
        confidence_scale.grid(row=0, column=1, padx=5, pady=5)
        
        self.confidence_label = ttk.Label(yolo_frame, text="0.8")
        self.confidence_label.grid(row=0, column=2, padx=5, pady=5)
        confidence_scale.configure(command=self.update_confidence_label)
        
        ttk.Label(yolo_frame, text="NMS Threshold:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.nms_var = tk.DoubleVar(value=0.4)
        nms_scale = ttk.Scale(yolo_frame, from_=0.1, to=1.0, variable=self.nms_var, 
                            orient=tk.HORIZONTAL, length=200)
        nms_scale.grid(row=1, column=1, padx=5, pady=5)
        
        self.nms_label = ttk.Label(yolo_frame, text="0.4")
        self.nms_label.grid(row=1, column=2, padx=5, pady=5)
        nms_scale.configure(command=self.update_nms_label)
        
    def create_alert_settings(self, parent):
        """Create alert settings"""
        # Email settings
        email_frame = ttk.LabelFrame(parent, text="Email Notifications")
        email_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(email_frame, text="SMTP Server:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.smtp_server_var = tk.StringVar(value="smtp.gmail.com")
        ttk.Entry(email_frame, textvariable=self.smtp_server_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(email_frame, text="SMTP Port:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.smtp_port_var = tk.StringVar(value="587")
        ttk.Entry(email_frame, textvariable=self.smtp_port_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(email_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(email_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_password_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.email_password_var, width=30, show="*").grid(row=3, column=1, padx=5, pady=5)
        
    def start_background_processes(self):
        """Start background processes"""
        # Update GUI periodically
        self.update_gui()
        
    def update_gui(self):
        """Update GUI elements periodically"""
        try:
            # Update dashboard stats
            self.update_dashboard_stats()
            
            # Update faculty list
            self.update_faculty_list()
            
            # Update alerts
            self.update_alerts_display()
            
            # Update camera feed if monitoring is active
            if self.monitoring_active:
                self.update_camera_feed()
                
        except Exception as e:
            print(f"Error updating GUI: {e}")
            
        # Schedule next update
        self.root.after(1000, self.update_gui)
        
    def update_dashboard_stats(self):
        """Update dashboard statistics"""
        try:
            faculty_count = len(self.faculty_manager.get_all_faculty())
            self.stats_labels["total_faculty"].config(text=str(faculty_count))
            
            camera_status = "Active" if self.monitoring_active else "Inactive"
            self.stats_labels["active_cameras"].config(text="1" if self.monitoring_active else "0")
            
            detections_today = len([d for d in self.detection_log 
                                  if d.get('date') == datetime.now().strftime('%Y-%m-%d')])
            self.stats_labels["detections_today"].config(text=str(detections_today))
            
            system_status = "Running" if self.monitoring_active else "Stopped"
            self.stats_labels["system_status"].config(text=system_status)
            
        except Exception as e:
            print(f"Error updating dashboard stats: {e}")
            
    def update_faculty_list(self):
        """Update faculty list in the treeview"""
        try:
            # Clear existing items
            for item in self.faculty_tree.get_children():
                self.faculty_tree.delete(item)
                
            # Add faculty members
            faculty_list = self.faculty_manager.get_all_faculty()
            for faculty in faculty_list:
                self.faculty_tree.insert("", tk.END, values=(
                    faculty.get('id', ''),
                    faculty.get('name', ''),
                    faculty.get('department', ''),
                    faculty.get('email', ''),
                    faculty.get('status', 'Active'),
                    faculty.get('last_seen', 'Never')
                ))
                
        except Exception as e:
            print(f"Error updating faculty list: {e}")
            
    def update_alerts_display(self):
        """Update alerts display"""
        try:
            # Clear existing items
            for item in self.alerts_tree.get_children():
                self.alerts_tree.delete(item)
                
            # Add alerts
            alerts = self.alert_system.get_all_alerts()
            for alert in alerts:
                self.alerts_tree.insert("", tk.END, values=(
                    alert.get('timestamp', ''),
                    alert.get('type', ''),
                    alert.get('priority', ''),
                    alert.get('message', ''),
                    alert.get('status', 'Active')
                ))
                
        except Exception as e:
            print(f"Error updating alerts display: {e}")
            
    def update_camera_feed(self):
        """Update camera feed display"""
        try:
            if self.current_frame is not None:
                # Convert frame to PhotoImage
                frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                
                # Resize frame to fit display
                display_size = (640, 480)
                frame_pil = frame_pil.resize(display_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(frame_pil)
                
                # Update label
                self.camera_label.configure(image=photo, text="")
                self.camera_label.image = photo  # Keep a reference
                
        except Exception as e:
            print(f"Error updating camera feed: {e}")
            
    def start_monitoring(self):
        """Start camera monitoring"""
        try:
            if not self.monitoring_active:
                self.monitoring_active = True
                
                # Start camera monitoring
                self.camera_monitor.start_monitoring()
                
                # Start ML processing
                self.ml_processor.start_processing()
                
                # Update UI
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.monitoring_status_label.config(text="Status: Running", foreground="green")
                
                # Start monitoring thread
                self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
                self.monitoring_thread.start()
                
                self.add_activity_log("Monitoring started")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")
            
    def stop_monitoring(self):
        """Stop camera monitoring"""
        try:
            if self.monitoring_active:
                self.monitoring_active = False
                
                # Stop camera monitoring
                self.camera_monitor.stop_monitoring()
                
                # Stop ML processing
                self.ml_processor.stop_processing()
                
                # Update UI
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.monitoring_status_label.config(text="Status: Stopped", foreground="red")
                
                # Clear camera display
                self.camera_label.configure(image="", text="Camera feed will appear here")
                
                self.add_activity_log("Monitoring stopped")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {e}")
            
    def monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Get frame from camera
                frame = self.camera_monitor.get_current_frame()
                
                if frame is not None:
                    self.current_frame = frame
                    
                    # Process frame with ML
                    detections = self.ml_processor.process_frame(frame)
                    
                    # Handle detections
                    for detection in detections:
                        self.handle_detection(detection)
                        
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                
    def handle_detection(self, detection):
        """Handle a face detection"""
        try:
            # Add to detection log
            detection_entry = {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'name': detection.get('name', 'Unknown'),
                'confidence': detection.get('confidence', 0.0),
                'camera': 'PC Camera'
            }
            
            self.detection_log.append(detection_entry)
            
            # Update detection listbox
            detection_text = f"{detection_entry['timestamp']} - {detection_entry['name']} ({detection_entry['confidence']:.2f})"
            self.detection_listbox.insert(0, detection_text)
            
            # Keep only last 100 entries
            if self.detection_listbox.size() > 100:
                self.detection_listbox.delete(tk.END)
                
            # Add to activity log
            self.add_activity_log(f"Detected: {detection_entry['name']}")
            
            # Check if alert should be generated
            if detection_entry['name'] == 'Unknown' or detection_entry['confidence'] < 0.7:
                self.alert_system.create_alert(
                    alert_type="Unknown Person",
                    message=f"Unknown person detected with confidence {detection_entry['confidence']:.2f}",
                    priority="Medium"
                )
                
        except Exception as e:
            print(f"Error handling detection: {e}")
            
    def add_activity_log(self, message):
        """Add message to activity log"""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            log_entry = f"{timestamp} - {message}"
            
            self.activity_listbox.insert(0, log_entry)
            
            # Keep only last 50 entries
            if self.activity_listbox.size() > 50:
                self.activity_listbox.delete(tk.END)
                
        except Exception as e:
            print(f"Error adding activity log: {e}")
            
    def add_faculty_dialog(self):
        """Show add faculty dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Faculty Member")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        fields = [
            ("Name:", "name"),
            ("Department:", "department"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Employee ID:", "employee_id")
        ]
        
        entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(dialog, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field_name] = entry
            
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        def save_faculty():
            faculty_data = {}
            for field_name, entry in entries.items():
                faculty_data[field_name] = entry.get()
                
            if faculty_data['name'] and faculty_data['email']:
                self.faculty_manager.add_faculty(faculty_data)
                dialog.destroy()
                messagebox.showinfo("Success", "Faculty member added successfully!")
            else:
                messagebox.showerror("Error", "Name and Email are required!")
                
        ttk.Button(button_frame, text="Save", command=save_faculty).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def edit_faculty_dialog(self):
        """Show edit faculty dialog"""
        selection = self.faculty_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a faculty member to edit.")
            return
            
        # Get selected faculty data
        item = self.faculty_tree.item(selection[0])
        faculty_id = item['values'][0]
        faculty_data = self.faculty_manager.get_faculty_by_id(faculty_id)
        
        if not faculty_data:
            messagebox.showerror("Error", "Faculty member not found.")
            return
            
        # Create edit dialog (similar to add dialog but pre-filled)
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Faculty Member")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields with existing data
        fields = [
            ("Name:", "name"),
            ("Department:", "department"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Employee ID:", "employee_id")
        ]
        
        entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(dialog, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, faculty_data.get(field_name, ''))
            entries[field_name] = entry
            
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        def update_faculty():
            updated_data = {'id': faculty_id}
            for field_name, entry in entries.items():
                updated_data[field_name] = entry.get()
                
            if updated_data['name'] and updated_data['email']:
                self.faculty_manager.update_faculty(faculty_id, updated_data)
                dialog.destroy()
                messagebox.showinfo("Success", "Faculty member updated successfully!")
            else:
                messagebox.showerror("Error", "Name and Email are required!")
                
        ttk.Button(button_frame, text="Update", command=update_faculty).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def delete_faculty(self):
        """Delete selected faculty member"""
        selection = self.faculty_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a faculty member to delete.")
            return
            
        item = self.faculty_tree.item(selection[0])
        faculty_id = item['values'][0]
        faculty_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {faculty_name}?"):
            self.faculty_manager.delete_faculty(faculty_id)
            messagebox.showinfo("Success", "Faculty member deleted successfully!")
            
    def upload_reference_image(self):
        """Upload reference image for faculty member"""
        selection = self.faculty_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a faculty member first.")
            return
            
        item = self.faculty_tree.item(selection[0])
        faculty_id = item['values'][0]
        faculty_name = item['values'][1]
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            # Process reference image
            success = self.ml_processor.process_reference_image(faculty_name, file_path)
            if success:
                messagebox.showinfo("Success", f"Reference image uploaded for {faculty_name}!")
            else:
                messagebox.showerror("Error", "Failed to process reference image.")
                
    def take_screenshot(self):
        """Take screenshot of current camera feed"""
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.jpg"
            
            # Save screenshot
            cv2.imwrite(filename, self.current_frame)
            messagebox.showinfo("Success", f"Screenshot saved as {filename}")
        else:
            messagebox.showwarning("Warning", "No camera feed available.")
            
    def clear_alerts(self):
        """Clear all alerts"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all alerts?"):
            self.alert_system.clear_all_alerts()
            messagebox.showinfo("Success", "All alerts cleared!")
            
    def export_alerts(self):
        """Export alerts to file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Alerts",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")]
        )
        
        if file_path:
            alerts = self.alert_system.get_all_alerts()
            
            if file_path.endswith('.json'):
                with open(file_path, 'w') as f:
                    json.dump(alerts, f, indent=2)
            elif file_path.endswith('.csv'):
                import csv
                with open(file_path, 'w', newline='') as f:
                    if alerts:
                        writer = csv.DictWriter(f, fieldnames=alerts[0].keys())
                        writer.writeheader()
                        writer.writerows(alerts)
                        
            messagebox.showinfo("Success", f"Alerts exported to {file_path}")
            
    def filter_alerts(self, event=None):
        """Filter alerts by priority"""
        # Implementation for filtering alerts
        pass
        
    def update_confidence_label(self, value):
        """Update confidence threshold label"""
        self.confidence_label.config(text=f"{float(value):.2f}")
        
    def update_nms_label(self, value):
        """Update NMS threshold label"""
        self.nms_label.config(text=f"{float(value):.2f}")
        
    def save_settings(self):
        """Save all settings"""
        try:
            settings = {
                'camera': {
                    'index': int(self.camera_index_var.get()),
                    'resolution': self.resolution_var.get(),
                    'fps': int(self.fps_var.get())
                },
                'detection': {
                    'confidence_threshold': self.confidence_var.get(),
                    'nms_threshold': self.nms_var.get()
                },
                'email': {
                    'smtp_server': self.smtp_server_var.get(),
                    'smtp_port': int(self.smtp_port_var.get()),
                    'email': self.email_var.get(),
                    'password': self.email_password_var.get()
                }
            }
            
            self.config.save_settings(settings)
            
            # Update components with new settings
            self.camera_monitor.update_settings(settings['camera'])
            self.ml_processor.update_settings(settings['detection'])
            self.alert_system.update_settings(settings['email'])
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

def main():
    root = tk.Tk()
    app = FacultyMonitoringApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
