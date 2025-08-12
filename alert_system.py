import json
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

class AlertSystem:
    def __init__(self, alerts_file='alerts.json'):
        self.alerts_file = alerts_file
        self.alerts = []
        self.alert_settings = {
            'enabled': True,
            'email_notifications': True,
            'sms_notifications': False,
            'alert_threshold_hours': 2,
            'high_priority_threshold_hours': 4,
            'email_server': 'smtp.gmail.com',
            'email_port': 587,
            'email_username': '',
            'email_password': '',
            'notification_recipients': []
        }
        
        self.load_alerts()
        self.load_settings()
        
    def load_alerts(self):
        """Load alerts from file"""
        if os.path.exists(self.alerts_file):
            try:
                with open(self.alerts_file, 'r') as f:
                    self.alerts = json.load(f)
            except Exception as e:
                print(f"Error loading alerts: {e}")
                self.alerts = []
        else:
            self.alerts = []
            
    def save_alerts(self):
        """Save alerts to file"""
        try:
            with open(self.alerts_file, 'w') as f:
                json.dump(self.alerts, f, indent=2)
        except Exception as e:
            print(f"Error saving alerts: {e}")
            
    def load_settings(self):
        """Load alert settings"""
        settings_file = 'alert_settings.json'
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    self.alert_settings.update(loaded_settings)
            except Exception as e:
                print(f"Error loading alert settings: {e}")
                
    def save_settings(self):
        """Save alert settings"""
        try:
            with open('alert_settings.json', 'w') as f:
                json.dump(self.alert_settings, f, indent=2)
        except Exception as e:
            print(f"Error saving alert settings: {e}")
            
    def add_alert(self, alert_data):
        """Add new alert"""
        if not self.alert_settings['enabled']:
            return False
            
        # Add metadata
        alert_data['created_at'] = datetime.now().isoformat()
        alert_data['id'] = len(self.alerts) + 1
        
        # Determine alert type and priority if not specified
        if 'type' not in alert_data:
            alert_data['type'] = 'general'
            
        if 'priority' not in alert_data:
            alert_data['priority'] = self.determine_priority(alert_data)
            
        self.alerts.append(alert_data)
        self.save_alerts()
        
        # Send notifications
        if self.alert_settings['email_notifications']:
            self.send_email_notification(alert_data)
            
        if self.alert_settings['sms_notifications']:
            self.send_sms_notification(alert_data)
            
        print(f"Alert created: {alert_data['title']}")
        return True
        
    def determine_priority(self, alert_data):
        """Determine alert priority based on content"""
        title = alert_data.get('title', '').lower()
        description = alert_data.get('description', '').lower()
        
        # High priority keywords
        high_priority_keywords = [
            'emergency', 'urgent', 'critical', 'security', 'unauthorized',
            'multiple', 'extended absence', 'system failure'
        ]
        
        # Medium priority keywords
        medium_priority_keywords = [
            'unknown person', 'not detected', 'camera', 'connection'
        ]
        
        for keyword in high_priority_keywords:
            if keyword in title or keyword in description:
                return 'high'
                
        for keyword in medium_priority_keywords:
            if keyword in title or keyword in description:
                return 'medium'
                
        return 'low'
        
    def update_alert_status(self, alert_title, new_status):
        """Update alert status"""
        for alert in self.alerts:
            if alert['title'] == alert_title:
                alert['status'] = new_status
                alert['updated_at'] = datetime.now().isoformat()
                
                if new_status in ['resolved', 'dismissed']:
                    alert['resolved_at'] = datetime.now().isoformat()
                    
                self.save_alerts()
                return True
        return False
        
    def get_alerts(self, status_filter=None, priority_filter=None):
        """Get alerts with optional filtering"""
        filtered_alerts = self.alerts
        
        if status_filter:
            filtered_alerts = [a for a in filtered_alerts if a['status'] == status_filter]
            
        if priority_filter:
            filtered_alerts = [a for a in filtered_alerts if a['priority'] == priority_filter]
            
        # Sort by creation time (newest first)
        filtered_alerts.sort(key=lambda x: x['created_at'], reverse=True)
        return filtered_alerts
        
    def get_active_alerts(self):
        """Get all active alerts"""
        return [a for a in self.alerts if a['status'] == 'active']
        
    def get_high_priority_alerts(self):
        """Get high priority active alerts"""
        return [a for a in self.alerts if a['status'] == 'active' and a['priority'] == 'high']
        
    def check_faculty_absence(self, faculty_manager):
        """Check for faculty absence and create alerts"""
        if not self.alert_settings['enabled']:
            return
            
        current_time = datetime.now()
        threshold_hours = self.alert_settings['alert_threshold_hours']
        high_priority_hours = self.alert_settings['high_priority_threshold_hours']
        
        for faculty in faculty_manager.get_all_faculty():
            if faculty['status'] == 'absent':
                # Check if we already have an active alert for this faculty
                existing_alert = None
                for alert in self.alerts:
                    if (alert['status'] == 'active' and 
                        alert.get('faculty_name') == faculty['name'] and
                        alert['type'] == 'absence'):
                        existing_alert = alert
                        break
                        
                if not existing_alert:
                    # Calculate absence duration (simplified)
                    # In real implementation, you'd parse the last_seen timestamp
                    absence_hours = threshold_hours + 1  # Simulate exceeding threshold
                    
                    if absence_hours >= threshold_hours:
                        priority = 'high' if absence_hours >= high_priority_hours else 'medium'
                        
                        alert_data = {
                            'type': 'absence',
                            'title': f'Faculty Absence Alert - {faculty["name"]}',
                            'description': f'{faculty["name"]} has been absent for {absence_hours} hours',
                            'priority': priority,
                            'status': 'active',
                            'faculty_name': faculty['name'],
                            'absence_hours': absence_hours
                        }
                        
                        self.add_alert(alert_data)
                        
    def create_unknown_person_alert(self, camera_name, confidence=0.5):
        """Create alert for unknown person detection"""
        alert_data = {
            'type': 'unknown_person',
            'title': 'Unknown Person Detected',
            'description': f'Unrecognized individual detected at {camera_name} (confidence: {confidence:.2f})',
            'priority': 'medium' if confidence > 0.7 else 'low',
            'status': 'active',
            'camera': camera_name,
            'confidence': confidence
        }
        
        self.add_alert(alert_data)
        
    def create_system_alert(self, component, issue, priority='medium'):
        """Create system-related alert"""
        alert_data = {
            'type': 'system_error',
            'title': f'System Issue - {component}',
            'description': issue,
            'priority': priority,
            'status': 'active',
            'component': component
        }
        
        self.add_alert(alert_data)
        
    def send_email_notification(self, alert_data):
        """Send email notification for alert"""
        try:
            if not self.alert_settings['email_username'] or not self.alert_settings['notification_recipients']:
                print("Email settings not configured")
                return False
                
            # Create message
            msg = MimeMultipart()
            msg['From'] = self.alert_settings['email_username']
            msg['To'] = ', '.join(self.alert_settings['notification_recipients'])
            msg['Subject'] = f"Faculty Monitoring Alert: {alert_data['title']}"
            
            # Email body
            body = f"""
            Alert Details:
            
            Title: {alert_data['title']}
            Priority: {alert_data['priority'].upper()}
            Description: {alert_data['description']}
            Time: {alert_data['timestamp']}
            
            Please check the Faculty Monitoring System for more details.
            
            This is an automated message from the Faculty Monitoring System.
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.alert_settings['email_server'], self.alert_settings['email_port'])
            server.starttls()
            server.login(self.alert_settings['email_username'], self.alert_settings['email_password'])
            text = msg.as_string()
            server.sendmail(self.alert_settings['email_username'], 
                          self.alert_settings['notification_recipients'], text)
            server.quit()
            
            print(f"Email notification sent for alert: {alert_data['title']}")
            return True
            
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False
            
    def send_sms_notification(self, alert_data):
        """Send SMS notification for alert"""
        # SMS implementation would go here
        # This would typically use a service like Twilio
        print(f"SMS notification would be sent for: {alert_data['title']}")
        
    def cleanup_old_alerts(self, days_to_keep=30):
        """Remove old resolved/dismissed alerts"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        original_count = len(self.alerts)
        self.alerts = [
            alert for alert in self.alerts
            if (alert['status'] == 'active' or 
                datetime.fromisoformat(alert['created_at']) > cutoff_date)
        ]
        
        removed_count = original_count - len(self.alerts)
        if removed_count > 0:
            self.save_alerts()
            print(f"Cleaned up {removed_count} old alerts")
            
    def get_alert_statistics(self):
        """Get alert statistics"""
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts if a['status'] == 'active'])
        resolved_alerts = len([a for a in self.alerts if a['status'] == 'resolved'])
        dismissed_alerts = len([a for a in self.alerts if a['status'] == 'dismissed'])
        
        priority_counts = {
            'high': len([a for a in self.alerts if a['priority'] == 'high']),
            'medium': len([a for a in self.alerts if a['priority'] == 'medium']),
            'low': len([a for a in self.alerts if a['priority'] == 'low'])
        }
        
        type_counts = {}
        for alert in self.alerts:
            alert_type = alert.get('type', 'general')
            type_counts[alert_type] = type_counts.get(alert_type, 0) + 1
            
        return {
            'total': total_alerts,
            'active': active_alerts,
            'resolved': resolved_alerts,
            'dismissed': dismissed_alerts,
            'by_priority': priority_counts,
            'by_type': type_counts
        }
        
    def update_settings(self, new_settings):
        """Update alert system settings"""
        self.alert_settings.update(new_settings)
        self.save_settings()
        print("Alert settings updated")
