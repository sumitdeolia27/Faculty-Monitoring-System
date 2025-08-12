import json
import os
from datetime import datetime

class FacultyManager:
    def __init__(self, data_file='faculty_data.json'):
        self.data_file = data_file
        self.faculty_list = []
        self.load_data()
        
    def load_data(self):
        """Load faculty data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.faculty_list = json.load(f)
            except Exception as e:
                print(f"Error loading faculty data: {e}")
                self.faculty_list = []
        else:
            self.faculty_list = []
            
    def save_data(self):
        """Save faculty data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.faculty_list, f, indent=2)
        except Exception as e:
            print(f"Error saving faculty data: {e}")
            
    def add_faculty(self, faculty_data):
        """Add new faculty member"""
        # Check if faculty already exists
        for faculty in self.faculty_list:
            if faculty['name'] == faculty_data['name']:
                return False
                
        # Add timestamp
        faculty_data['created_at'] = datetime.now().isoformat()
        faculty_data['id'] = len(self.faculty_list) + 1
        
        self.faculty_list.append(faculty_data)
        self.save_data()
        return True
        
    def update_faculty(self, faculty_id, updated_data):
        """Update existing faculty member"""
        for i, faculty in enumerate(self.faculty_list):
            if faculty['id'] == faculty_id:
                self.faculty_list[i].update(updated_data)
                self.faculty_list[i]['updated_at'] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
        
    def delete_faculty(self, faculty_name):
        """Delete faculty member by name"""
        self.faculty_list = [f for f in self.faculty_list if f['name'] != faculty_name]
        self.save_data()
        
    def get_faculty_by_name(self, name):
        """Get faculty member by name"""
        for faculty in self.faculty_list:
            if faculty['name'] == name:
                return faculty
        return None
        
    def get_all_faculty(self):
        """Get all faculty members"""
        return self.faculty_list
        
    def update_presence_status(self, faculty_name, status, timestamp=None):
        """Update faculty presence status"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
            
        for faculty in self.faculty_list:
            if faculty['name'] == faculty_name:
                faculty['status'] = status
                faculty['last_seen'] = timestamp
                self.save_data()
                return True
        return False
        
    def update_image_status(self, faculty_name, has_image):
        """Update faculty image upload status"""
        for faculty in self.faculty_list:
            if faculty['name'] == faculty_name:
                faculty['image_uploaded'] = has_image
                self.save_data()
                return True
        return False
        
    def get_present_faculty(self):
        """Get list of currently present faculty"""
        return [f for f in self.faculty_list if f['status'] == 'present']
        
    def get_absent_faculty(self):
        """Get list of currently absent faculty"""
        return [f for f in self.faculty_list if f['status'] == 'absent']
        
    def search_faculty(self, search_term):
        """Search faculty by name or department"""
        search_term = search_term.lower()
        results = []
        
        for faculty in self.faculty_list:
            if (search_term in faculty['name'].lower() or 
                search_term in faculty['department'].lower()):
                results.append(faculty)
                
        return results
