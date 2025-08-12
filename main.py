import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import json
import os
from faculty_manager import FacultyManager
from camera_monitor import CameraMonitor
from alert_system import AlertSystem
from ml_processor import MLProcessor

class FacultyMonitoringSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Faculty Presence Monitoring & Alert System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.faculty_manager = FacultyManager()
        self.camera_monitor = CameraMonitor()
        self.alert_system = AlertSystem()
        self.ml_processor = MLProcessor()
        
        # System state
        self.monitoring_active = False
        self.detection_thread = None
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_faculty_tab()
        self.create_monitoring_tab()
        self.create_alerts_tab()
        self.create_settings_tab()
        
    def create_dashboard_tab(self):
        # Dashboard tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_label = tk.Label(dashboard_frame, text="Faculty Monitoring Dashboard", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(dashboard_frame, bg='#f0f0f0')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Create stat cards
        self.create_stat_card(stats_frame, "Total Faculty", "24", "#3498db", 0, 0)
        self.create_stat_card(stats_frame, "Present Today", "18", "#27ae60", 0, 1)
        self.create_stat_card(stats_frame, "Active Cameras", "8", "#9b59b6", 0, 2)
        self.create_stat_card(stats_frame, "Alerts Today", "3", "#e74c3c", 0, 3)
        
        # Recent activity frame
        activity_frame = tk.LabelFrame(dashboard_frame, text="Recent Activity", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0')
        activity_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Activity listbox
        self.activity_listbox = tk.Listbox(activity_frame, font=('Arial', 10), height=10)
        self.activity_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # System status frame
        status_frame = tk.LabelFrame(dashboard_frame, text="System Status", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_labels = {}
        status_items = [
            ("OpenCV Capture", "Active"),
            ("YOLOv8 Detection", "Running"),
            ("DeepFace Verification", "Online"),
            ("Alert System", "Ready")
        ]
        
        for i, (component, status) in enumerate(status_items):
            row_frame = tk.Frame(status_frame, bg='#f0f0f0')
            row_frame.pack(fill='x', padx=10, pady=2)
            
            tk.Label(row_frame, text=component, font=('Arial', 10), 
                    bg='#f0f0f0', anchor='w').pack(side='left')
            
            status_label = tk.Label(row_frame, text=status, font=('Arial', 10, 'bold'), 
                                  fg='#27ae60', bg='#f0f0f0', anchor='e')
            status_label.pack(side='right')
            self.status_labels[component] = status_label
            
    def create_stat_card(self, parent, title, value, color, row, col):
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(card_frame, text=title, font=('Arial', 10, 'bold'), 
                bg=color, fg='white').pack(pady=(10, 5))
        tk.Label(card_frame, text=value, font=('Arial', 18, 'bold'), 
                bg=color, fg='white').pack(pady=(0, 10))
        
    def create_faculty_tab(self):
        # Faculty management tab
        faculty_frame = ttk.Frame(self.notebook)
        self.notebook.add(faculty_frame, text="Faculty Management")
        
        # Title and controls
        title_frame = tk.Frame(faculty_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="Faculty Management", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0').pack(side='left')
        
        tk.Button(title_frame, text="Add Faculty", command=self.add_faculty_dialog,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='right')
        
        # Search frame
        search_frame = tk.Frame(faculty_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_faculty)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=10)
        
        # Faculty list
        list_frame = tk.Frame(faculty_frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for faculty list
        columns = ('Name', 'Department', 'Email', 'Status', 'Last Seen', 'Image')
        self.faculty_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.faculty_tree.heading(col, text=col)
            self.faculty_tree.column(col, width=150)
            
        self.faculty_tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.faculty_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.faculty_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = tk.Frame(faculty_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(buttons_frame, text="Edit", command=self.edit_faculty,
                 bg='#f39c12', fg='white').pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Delete", command=self.delete_faculty,
                 bg='#e74c3c', fg='white').pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Upload Image", command=self.upload_image,
                 bg='#9b59b6', fg='white').pack(side='left', padx=5)
        
    def create_monitoring_tab(self):
        # Live monitoring tab
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="Live Monitoring")
        
        # Control frame
        control_frame = tk.Frame(monitoring_frame, bg='#f0f0f0')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(control_frame, text="Live Monitoring", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0').pack(side='left')
        
        self.monitor_button = tk.Button(control_frame, text="Start Monitoring", 
                                       command=self.toggle_monitoring,
                                       bg='#27ae60', fg='white', font=('Arial', 10, 'bold'))
        self.monitor_button.pack(side='right')
        
        # Status indicator
        self.monitor_status = tk.Label(control_frame, text="● Monitoring Stopped", 
                                      fg='#e74c3c', bg='#f0f0f0', font=('Arial', 10, 'bold'))
        self.monitor_status.pack(side='right', padx=20)
        
        # Main content frame
        content_frame = tk.Frame(monitoring_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Camera feeds frame (left side)
        cameras_frame = tk.LabelFrame(content_frame, text="Camera Feeds", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        cameras_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Camera grid
        self.camera_frames = {}
        cameras = [
            "Main Entrance", "Faculty Lounge", "Corridor A", 
            "Conference Room", "Library", "Cafeteria"
        ]
        
        for i, camera in enumerate(cameras):
            row, col = i // 2, i % 2
            camera_frame = tk.Frame(cameras_frame, bg='#2c3e50', relief='raised', bd=2)
            camera_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            tk.Label(camera_frame, text=camera, bg='#2c3e50', fg='white', 
                    font=('Arial', 10, 'bold')).pack(pady=10)
            tk.Label(camera_frame, text="📹", bg='#2c3e50', fg='white', 
                    font=('Arial', 24)).pack(pady=20)
            
            status_label = tk.Label(camera_frame, text="Active", bg='#27ae60', 
                                  fg='white', font=('Arial', 8, 'bold'))
            status_label.pack(pady=5)
            
            self.camera_frames[camera] = camera_frame
            
        for i in range(2):
            cameras_frame.grid_columnconfigure(i, weight=1)
            
        # Detection log frame (right side)
        log_frame = tk.LabelFrame(content_frame, text="Detection Log", 
                                font=('Arial', 12, 'bold'), bg='#f0f0f0')
        log_frame.pack(side='right', fill='y', padx=(10, 0))
        
        self.detection_listbox = tk.Listbox(log_frame, width=40, height=20, 
                                          font=('Arial', 9))
        self.detection_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clear button
        tk.Button(log_frame, text="Clear Log", command=self.clear_detection_log,
                 bg='#95a5a6', fg='white').pack(pady=5)
        
    def create_alerts_tab(self):
        # Alerts tab
        alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(alerts_frame, text="Alerts")
        
        # Title and stats
        title_frame = tk.Frame(alerts_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="Alert Management", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0').pack(side='left')
        
        self.alert_count_label = tk.Label(title_frame, text="3 Active Alerts", 
                                        fg='#e74c3c', bg='#f0f0f0', font=('Arial', 12, 'bold'))
        self.alert_count_label.pack(side='right')
        
        # Filter frame
        filter_frame = tk.Frame(alerts_frame, bg='#f0f0f0')
        filter_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(filter_frame, text="Filter:", bg='#f0f0f0').pack(side='left')
        
        self.alert_filter = ttk.Combobox(filter_frame, values=['All', 'Active', 'Resolved', 'Dismissed'])
        self.alert_filter.set('All')
        self.alert_filter.pack(side='left', padx=10)
        self.alert_filter.bind('<<ComboboxSelected>>', self.filter_alerts)
        
        # Alerts list
        alerts_list_frame = tk.Frame(alerts_frame, bg='#f0f0f0')
        alerts_list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for alerts
        alert_columns = ('Type', 'Title', 'Description', 'Time', 'Status', 'Priority')
        self.alerts_tree = ttk.Treeview(alerts_list_frame, columns=alert_columns, 
                                       show='headings', height=15)
        
        for col in alert_columns:
            self.alerts_tree.heading(col, text=col)
            self.alerts_tree.column(col, width=150)
            
        self.alerts_tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for alerts
        alert_scrollbar = ttk.Scrollbar(alerts_list_frame, orient='vertical', 
                                       command=self.alerts_tree.yview)
        alert_scrollbar.pack(side='right', fill='y')
        self.alerts_tree.configure(yscrollcommand=alert_scrollbar.set)
        
        # Alert action buttons
        alert_buttons_frame = tk.Frame(alerts_frame, bg='#f0f0f0')
        alert_buttons_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(alert_buttons_frame, text="Resolve", command=self.resolve_alert,
                 bg='#27ae60', fg='white').pack(side='left', padx=5)
        tk.Button(alert_buttons_frame, text="Dismiss", command=self.dismiss_alert,
                 bg='#95a5a6', fg='white').pack(side='left', padx=5)
        
    def create_settings_tab(self):
        # Settings tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Create notebook for settings categories
        settings_notebook = ttk.Notebook(settings_frame)
        settings_notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # AI Settings
        ai_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(ai_frame, text="AI & Detection")
        
        self.create_ai_settings(ai_frame)
        
        # Alert Settings
        alert_settings_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(alert_settings_frame, text="Alerts")
        
        self.create_alert_settings(alert_settings_frame)
        
        # Camera Settings
        camera_settings_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(camera_settings_frame, text="Cameras")
        
        self.create_camera_settings(camera_settings_frame)
        
    def create_ai_settings(self, parent):
        # Detection threshold
        tk.Label(parent, text="Detection Confidence Threshold:").pack(anchor='w', pady=5)
        self.detection_threshold = tk.Scale(parent, from_=0.1, to=1.0, resolution=0.1, 
                                          orient='horizontal', length=300)
        self.detection_threshold.set(0.8)
        self.detection_threshold.pack(anchor='w', pady=5)
        
        # Face detection model
        tk.Label(parent, text="Face Detection Model:").pack(anchor='w', pady=5)
        self.detection_model = ttk.Combobox(parent, values=['YOLOv8', 'MTCNN', 'OpenCV Haar'])
        self.detection_model.set('YOLOv8')
        self.detection_model.pack(anchor='w', pady=5)
        
        # Face verification model
        tk.Label(parent, text="Face Verification Model:").pack(anchor='w', pady=5)
        self.verification_model = ttk.Combobox(parent, values=['DeepFace', 'FaceNet', 'ArcFace'])
        self.verification_model.set('DeepFace')
        self.verification_model.pack(anchor='w', pady=5)
        
        # Processing interval
        tk.Label(parent, text="Processing Interval (ms):").pack(anchor='w', pady=5)
        self.processing_interval = tk.Spinbox(parent, from_=50, to=1000, value=100)
        self.processing_interval.pack(anchor='w', pady=5)
        
    def create_alert_settings(self, parent):
        # Enable alerts
        self.alerts_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(parent, text="Enable Alerts", variable=self.alerts_enabled).pack(anchor='w', pady=5)
        
        # Email notifications
        self.email_notifications = tk.BooleanVar(value=True)
        tk.Checkbutton(parent, text="Email Notifications", variable=self.email_notifications).pack(anchor='w', pady=5)
        
        # Alert threshold
        tk.Label(parent, text="Alert Threshold (hours):").pack(anchor='w', pady=5)
        self.alert_threshold = tk.Spinbox(parent, from_=1, to=24, value=2)
        self.alert_threshold.pack(anchor='w', pady=5)
        
        # High priority threshold
        tk.Label(parent, text="High Priority Threshold (hours):").pack(anchor='w', pady=5)
        self.high_priority_threshold = tk.Spinbox(parent, from_=2, to=48, value=4)
        self.high_priority_threshold.pack(anchor='w', pady=5)
        
    def create_camera_settings(self, parent):
        # Default FPS
        tk.Label(parent, text="Default Frame Rate (FPS):").pack(anchor='w', pady=5)
        self.default_fps = ttk.Combobox(parent, values=['15', '24', '30', '60'])
        self.default_fps.set('30')
        self.default_fps.pack(anchor='w', pady=5)
        
        # Recording enabled
        self.recording_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(parent, text="Enable Recording", variable=self.recording_enabled).pack(anchor='w', pady=5)
        
        # Recording duration
        tk.Label(parent, text="Recording Duration (hours):").pack(anchor='w', pady=5)
        self.recording_duration = tk.Spinbox(parent, from_=1, to=168, value=24)
        self.recording_duration.pack(anchor='w', pady=5)
        
        # Save settings button
        tk.Button(parent, text="Save Settings", command=self.save_settings,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
        
    def toggle_monitoring(self):
        if not self.monitoring_active:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        self.monitoring_active = True
        self.monitor_button.config(text="Stop Monitoring", bg='#e74c3c')
        self.monitor_status.config(text="● Monitoring Active", fg='#27ae60')
        
        # Start detection thread
        self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
        self.detection_thread.start()
        
        self.add_activity("System", "Monitoring started")
        
    def stop_monitoring(self):
        self.monitoring_active = False
        self.monitor_button.config(text="Start Monitoring", bg='#27ae60')
        self.monitor_status.config(text="● Monitoring Stopped", fg='#e74c3c')
        
        self.add_activity("System", "Monitoring stopped")
        
    def detection_loop(self):
        """Main detection loop running in separate thread"""
        while self.monitoring_active:
            try:
                # Simulate detection process
                detections = self.ml_processor.process_frame()
                
                for detection in detections:
                    self.add_detection(detection)
                    
                    # Check for alerts
                    if detection['confidence'] < 0.7:
                        self.create_alert("Unknown Person", 
                                        f"Low confidence detection: {detection['name']}", 
                                        "medium")
                        
                time.sleep(2)  # Process every 2 seconds
                
            except Exception as e:
                print(f"Detection error: {e}")
                time.sleep(1)
                
    def add_detection(self, detection):
        """Add detection to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        detection_text = f"[{timestamp}] {detection['name']} - {detection['confidence']:.2f} - {detection['camera']}"
        
        # Update UI in main thread
        self.root.after(0, lambda: self.detection_listbox.insert(0, detection_text))
        
        # Keep only last 50 detections
        self.root.after(0, lambda: self.detection_listbox.delete(50, tk.END) 
                       if self.detection_listbox.size() > 50 else None)
        
    def add_activity(self, person, action):
        """Add activity to dashboard"""
        timestamp = datetime.now().strftime("%H:%M")
        activity_text = f"[{timestamp}] {person} - {action}"
        self.activity_listbox.insert(0, activity_text)
        
        # Keep only last 20 activities
        if self.activity_listbox.size() > 20:
            self.activity_listbox.delete(20, tk.END)
            
    def create_alert(self, title, description, priority):
        """Create new alert"""
        alert = {
            'id': int(time.time()),
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'active',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.alert_system.add_alert(alert)
        self.refresh_alerts()
        
    def add_faculty_dialog(self):
        """Open dialog to add new faculty"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Faculty Member")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        
        # Form fields
        tk.Label(dialog, text="Name:", bg='#f0f0f0').pack(pady=5)
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Department:", bg='#f0f0f0').pack(pady=5)
        dept_entry = tk.Entry(dialog, width=40)
        dept_entry.pack(pady=5)
        
        tk.Label(dialog, text="Email:", bg='#f0f0f0').pack(pady=5)
        email_entry = tk.Entry(dialog, width=40)
        email_entry.pack(pady=5)
        
        tk.Label(dialog, text="Phone:", bg='#f0f0f0').pack(pady=5)
        phone_entry = tk.Entry(dialog, width=40)
        phone_entry.pack(pady=5)
        
        def save_faculty():
            faculty_data = {
                'name': name_entry.get(),
                'department': dept_entry.get(),
                'email': email_entry.get(),
                'phone': phone_entry.get(),
                'status': 'absent',
                'last_seen': 'Never',
                'image_uploaded': False
            }
            
            if faculty_data['name'] and faculty_data['department']:
                self.faculty_manager.add_faculty(faculty_data)
                self.refresh_faculty_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Faculty member added successfully!")
            else:
                messagebox.showerror("Error", "Name and Department are required!")
                
        tk.Button(dialog, text="Save", command=save_faculty,
                 bg='#3498db', fg='white').pack(pady=20)
        
    def refresh_faculty_list(self):
        """Refresh faculty list display"""
        # Clear existing items
        for item in self.faculty_tree.get_children():
            self.faculty_tree.delete(item)
            
        # Add faculty members
        for faculty in self.faculty_manager.get_all_faculty():
            self.faculty_tree.insert('', 'end', values=(
                faculty['name'],
                faculty['department'],
                faculty['email'],
                faculty['status'],
                faculty['last_seen'],
                'Yes' if faculty['image_uploaded'] else 'No'
            ))
            
    def refresh_alerts(self):
        """Refresh alerts display"""
        # Clear existing items
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
            
        # Add alerts
        alerts = self.alert_system.get_alerts()
        active_count = sum(1 for alert in alerts if alert['status'] == 'active')
        
        self.alert_count_label.config(text=f"{active_count} Active Alerts")
        
        for alert in alerts:
            self.alerts_tree.insert('', 'end', values=(
                alert.get('type', 'General'),
                alert['title'],
                alert['description'][:50] + '...' if len(alert['description']) > 50 else alert['description'],
                alert['timestamp'],
                alert['status'],
                alert['priority']
            ))
            
    def filter_faculty(self, *args):
        """Filter faculty list based on search"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.faculty_tree.get_children():
            self.faculty_tree.delete(item)
            
        # Add filtered faculty members
        for faculty in self.faculty_manager.get_all_faculty():
            if (search_term in faculty['name'].lower() or 
                search_term in faculty['department'].lower()):
                self.faculty_tree.insert('', 'end', values=(
                    faculty['name'],
                    faculty['department'],
                    faculty['email'],
                    faculty['status'],
                    faculty['last_seen'],
                    'Yes' if faculty['image_uploaded'] else 'No'
                ))
                
    def filter_alerts(self, event=None):
        """Filter alerts based on status"""
        filter_value = self.alert_filter.get()
        
        # Clear existing items
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
            
        # Add filtered alerts
        for alert in self.alert_system.get_alerts():
            if filter_value == 'All' or alert['status'].title() == filter_value:
                self.alerts_tree.insert('', 'end', values=(
                    alert.get('type', 'General'),
                    alert['title'],
                    alert['description'][:50] + '...' if len(alert['description']) > 50 else alert['description'],
                    alert['timestamp'],
                    alert['status'],
                    alert['priority']
                ))
                
    def edit_faculty(self):
        """Edit selected faculty member"""
        selection = self.faculty_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a faculty member to edit.")
            return
            
        # Get selected faculty data
        item = self.faculty_tree.item(selection[0])
        faculty_name = item['values'][0]
        
        messagebox.showinfo("Info", f"Edit functionality for {faculty_name} would be implemented here.")
        
    def delete_faculty(self):
        """Delete selected faculty member"""
        selection = self.faculty_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a faculty member to delete.")
            return
            
        item = self.faculty_tree.item(selection[0])
        faculty_name = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {faculty_name}?"):
            self.faculty_manager.delete_faculty(faculty_name)
            self.refresh_faculty_list()
            
    def upload_image(self):
        """Upload reference image for selected faculty"""
        selection = self.faculty_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a faculty member.")
            return
            
        item = self.faculty_tree.item(selection[0])
        faculty_name = item['values'][0]
        
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            # Process and save the image
            success = self.ml_processor.process_reference_image(faculty_name, file_path)
            if success:
                self.faculty_manager.update_image_status(faculty_name, True)
                self.refresh_faculty_list()
                messagebox.showinfo("Success", "Reference image uploaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to process image.")
                
    def resolve_alert(self):
        """Resolve selected alert"""
        selection = self.alerts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an alert to resolve.")
            return
            
        item = self.alerts_tree.item(selection[0])
        alert_title = item['values'][1]
        
        self.alert_system.update_alert_status(alert_title, 'resolved')
        self.refresh_alerts()
        
    def dismiss_alert(self):
        """Dismiss selected alert"""
        selection = self.alerts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an alert to dismiss.")
            return
            
        item = self.alerts_tree.item(selection[0])
        alert_title = item['values'][1]
        
        self.alert_system.update_alert_status(alert_title, 'dismissed')
        self.refresh_alerts()
        
    def clear_detection_log(self):
        """Clear detection log"""
        self.detection_listbox.delete(0, tk.END)
        
    def save_settings(self):
        """Save system settings"""
        settings = {
            'detection_threshold': self.detection_threshold.get(),
            'detection_model': self.detection_model.get(),
            'verification_model': self.verification_model.get(),
            'processing_interval': int(self.processing_interval.get()),
            'alerts_enabled': self.alerts_enabled.get(),
            'email_notifications': self.email_notifications.get(),
            'alert_threshold': int(self.alert_threshold.get()),
            'high_priority_threshold': int(self.high_priority_threshold.get()),
            'default_fps': int(self.default_fps.get()),
            'recording_enabled': self.recording_enabled.get(),
            'recording_duration': int(self.recording_duration.get())
        }
        
        # Save to file
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
            
        messagebox.showinfo("Success", "Settings saved successfully!")
        
    def load_data(self):
        """Load initial data"""
        # Load sample faculty data
        sample_faculty = [
            {
                'name': 'Dr. Sarah Wilson',
                'department': 'Computer Science',
                'email': 's.wilson@university.edu',
                'phone': '+1-234-567-8901',
                'status': 'present',
                'last_seen': '09:15 AM',
                'image_uploaded': True
            },
            {
                'name': 'Prof. John Miller',
                'department': 'Mathematics',
                'email': 'j.miller@university.edu',
                'phone': '+1-234-567-8902',
                'status': 'absent',
                'last_seen': 'Yesterday 5:30 PM',
                'image_uploaded': True
            },
            {
                'name': 'Dr. Emma Davis',
                'department': 'Physics',
                'email': 'e.davis@university.edu',
                'phone': '+1-234-567-8903',
                'status': 'present',
                'last_seen': '08:30 AM',
                'image_uploaded': False
            }
        ]
        
        for faculty in sample_faculty:
            self.faculty_manager.add_faculty(faculty)
            
        # Load sample alerts
        sample_alerts = [
            {
                'id': 1,
                'type': 'absence',
                'title': 'Faculty Not Detected',
                'description': 'Prof. Michael Brown has not been detected for 2 hours',
                'priority': 'high',
                'status': 'active',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'id': 2,
                'type': 'unknown_person',
                'title': 'Unknown Person Detected',
                'description': 'Unrecognized individual in faculty lounge',
                'priority': 'medium',
                'status': 'active',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        
        for alert in sample_alerts:
            self.alert_system.add_alert(alert)
            
        # Refresh displays
        self.refresh_faculty_list()
        self.refresh_alerts()
        
        # Add initial activities
        self.add_activity("System", "Application started")
        self.add_activity("Dr. Sarah Wilson", "Arrived")
        self.add_activity("Dr. Emma Davis", "Arrived")
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FacultyMonitoringSystem()
    app.run()
