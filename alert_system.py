import json
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
import threading

class AlertSystem:
    def __init__(self):
        self.alerts_file = "data/alerts.json"
        self.alerts = []
        self.email_settings = {}
        self.ensure_data_directory()
        self.load_alerts()
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
        
    def load_alerts(self):
        """Load alerts from file"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r') as f:
                    self.alerts = json.load(f)
                print(f"Loaded {len(self.alerts)} alerts")
            else:
                self.alerts = []
                
        except Exception as e:
            print(f"Error loading alerts: {e}")
            self.alerts = []
            
    def save_alerts(self):
        """Save alerts to file"""
        try:
            with open(self.alerts_file, 'w') as f:
                json.dump(self.alerts, f, indent=2)
                
        except Exception as e:
            print(f"Error saving alerts: {e}")
            
    def create_alert(self, alert_type, message, priority="Medium", auto_email=True):
        """Create a new alert"""
        try:
            alert = {
                'id': str(uuid.uuid4()),
                'type': alert_type,
                'message': message,
                'priority': priority,
                'status': 'Active',
                'timestamp': datetime.now().isoformat(),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.alerts.insert(0, alert)  # Add to beginning for newest first
            self.save_alerts()
            
            print(f"Alert created: {alert_type} - {message}")
            
            # Send email notification if enabled
            if auto_email and self.email_settings:
                threading.Thread(target=self.send_email_alert, args=(alert,), daemon=True).start()
                
            return alert['id']
            
        except Exception as e:
            print(f"Error creating alert: {e}")
            return None
            
    def resolve_alert(self, alert_id):
        """Resolve an alert"""
        try:
            for alert in self.alerts:
                if alert['id'] == alert_id:
                    alert['status'] = 'Resolved'
                    alert['resolved_at'] = datetime.now().isoformat()
                    self.save_alerts()
                    print(f"Alert resolved: {alert_id}")
                    return True
                    
            return False
            
        except Exception as e:
            print(f"Error resolving alert: {e}")
            return False
            
    def dismiss_alert(self, alert_id):
        """Dismiss an alert"""
        try:
            for alert in self.alerts:
                if alert['id'] == alert_id:
                    alert['status'] = 'Dismissed'
                    alert['dismissed_at'] = datetime.now().isoformat()
                    self.save_alerts()
                    print(f"Alert dismissed: {alert_id}")
                    return True
                    
            return False
            
        except Exception as e:
            print(f"Error dismissing alert: {e}")
            return False
            
    def get_all_alerts(self):
        """Get all alerts"""
        return self.alerts.copy()
        
    def get_active_alerts(self):
        """Get only active alerts"""
        return [alert for alert in self.alerts if alert['status'] == 'Active']
        
    def get_alerts_by_priority(self, priority):
        """Get alerts by priority"""
        return [alert for alert in self.alerts if alert['priority'] == priority]
        
    def get_alerts_by_type(self, alert_type):
        """Get alerts by type"""
        return [alert for alert in self.alerts if alert['type'] == alert_type]
        
    def clear_all_alerts(self):
        """Clear all alerts"""
        try:
            self.alerts = []
            self.save_alerts()
            print("All alerts cleared")
            return True
            
        except Exception as e:
            print(f"Error clearing alerts: {e}")
            return False
            
    def clear_resolved_alerts(self):
        """Clear only resolved alerts"""
        try:
            self.alerts = [alert for alert in self.alerts if alert['status'] != 'Resolved']
            self.save_alerts()
            print("Resolved alerts cleared")
            return True
            
        except Exception as e:
            print(f"Error clearing resolved alerts: {e}")
            return False
            
    def update_settings(self, email_settings):
        """Update email settings"""
        try:
            self.email_settings = email_settings
            print("Alert system email settings updated")
            
        except Exception as e:
            print(f"Error updating alert settings: {e}")
            
    def send_email_alert(self, alert):
        """Send email notification for alert"""
        try:
            if not self.email_settings or not all(key in self.email_settings for key in ['email', 'password', 'smtp_server', 'smtp_port']):
                print("Email settings not configured, skipping email notification")
                return False
                
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_settings['email']
            msg['To'] = self.email_settings['email']  # Send to same email for demo
            msg['Subject'] = f"Faculty Monitoring Alert: {alert['type']}"
            
            # Email body
            body = f"""
Faculty Monitoring System Alert

Type: {alert['type']}
Priority: {alert['priority']}
Time: {alert['created_at']}
Message: {alert['message']}

This is an automated alert from the Faculty Monitoring System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.email_settings['smtp_server'], self.email_settings['smtp_port'])
            server.starttls()
            server.login(self.email_settings['email'], self.email_settings['password'])
            
            text = msg.as_string()
            server.sendmail(self.email_settings['email'], self.email_settings['email'], text)
            server.quit()
            
            print(f"Email alert sent for: {alert['type']}")
            return True
            
        except Exception as e:
            print(f"Error sending email alert: {e}")
            return False
            
    def get_alert_statistics(self):
        """Get alert statistics"""
        try:
            total_alerts = len(self.alerts)
            active_alerts = len(self.get_active_alerts())
            resolved_alerts = len([a for a in self.alerts if a['status'] == 'Resolved'])
            dismissed_alerts = len([a for a in self.alerts if a['status'] == 'Dismissed'])
            
            priority_counts = {}
            for priority in ['High', 'Medium', 'Low']:
                priority_counts[priority] = len(self.get_alerts_by_priority(priority))
                
            return {
                'total': total_alerts,
                'active': active_alerts,
                'resolved': resolved_alerts,
                'dismissed': dismissed_alerts,
                'priority_counts': priority_counts
            }
            
        except Exception as e:
            print(f"Error getting alert statistics: {e}")
            return {}
            
    def cleanup_old_alerts(self, days=30):
        """Remove alerts older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            original_count = len(self.alerts)
            self.alerts = [
                alert for alert in self.alerts 
                if datetime.fromisoformat(alert['timestamp']) > cutoff_date
            ]
            
            removed_count = original_count - len(self.alerts)
            
            if removed_count > 0:
                self.save_alerts()
                print(f"Removed {removed_count} old alerts")
                
            return removed_count
            
        except Exception as e:
            print(f"Error cleaning up old alerts: {e}")
            return 0
