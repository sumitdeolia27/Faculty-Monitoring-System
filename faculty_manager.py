import json
import os
from datetime import datetime
import uuid

class FacultyManager:
    def __init__(self):
        self.data_file = "data/faculty_data.json"
        self.faculty_data = []
        self.ensure_data_directory()
        self.load_data()
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
        
    def load_data(self):
        """Load faculty data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.faculty_data = json.load(f)
                print(f"Loaded {len(self.faculty_data)} faculty members")
            else:
                # Create sample data
                self.create_sample_data()
                
        except Exception as e:
            print(f"Error loading faculty data: {e}")
            self.faculty_data = []
            
    def save_data(self):
        """Save faculty data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.faculty_data, f, indent=2)
            print("Faculty data saved successfully")
            
        except Exception as e:
            print(f"Error saving faculty data: {e}")
            
    def create_sample_data(self):
        """Create sample faculty data"""
        sample_faculty = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Dr. John Smith',
                'department': 'Computer Science',
                'email': 'john.smith@university.edu',
                'phone': '+1-555-0101',
                'employee_id': 'CS001',
                'status': 'Active',
                'created_at': datetime.now().isoformat(),
                'last_seen': 'Never'
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Prof. Sarah Johnson',
                'department': 'Mathematics',
                'email': 'sarah.johnson@university.edu',
                'phone': '+1-555-0102',
                'employee_id': 'MATH001',
                'status': 'Active',
                'created_at': datetime.now().isoformat(),
                'last_seen': 'Never'
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Dr. Michael Brown',
                'department': 'Physics',
                'email': 'michael.brown@university.edu',
                'phone': '+1-555-0103',
                'employee_id': 'PHY001',
                'status': 'Active',
                'created_at': datetime.now().isoformat(),
                'last_seen': 'Never'
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Prof. Emily Davis',
                'department': 'Chemistry',
                'email': 'emily.davis@university.edu',
                'phone': '+1-555-0104',
                'employee_id': 'CHEM001',
                'status': 'Active',
                'created_at': datetime.now().isoformat(),
                'last_seen': 'Never'
            }
        ]
        
        self.faculty_data = sample_faculty
        self.save_data()
        print("Sample faculty data created")
        
    def add_faculty(self, faculty_info):
        """Add new faculty member"""
        try:
            faculty_info['id'] = str(uuid.uuid4())
            faculty_info['status'] = 'Active'
            faculty_info['created_at'] = datetime.now().isoformat()
            faculty_info['last_seen'] = 'Never'
            
            self.faculty_data.append(faculty_info)
            self.save_data()
            
            print(f"Added faculty member: {faculty_info['name']}")
            return True
            
        except Exception as e:
            print(f"Error adding faculty member: {e}")
            return False
            
    def update_faculty(self, faculty_id, updated_info):
        """Update faculty member information"""
        try:
            for i, faculty in enumerate(self.faculty_data):
                if faculty['id'] == faculty_id:
                    # Preserve original creation data
                    updated_info['id'] = faculty_id
                    updated_info['created_at'] = faculty.get('created_at', datetime.now().isoformat())
                    updated_info['last_seen'] = faculty.get('last_seen', 'Never')
                    updated_info['updated_at'] = datetime.now().isoformat()
                    
                    self.faculty_data[i] = updated_info
                    self.save_data()
                    
                    print(f"Updated faculty member: {updated_info['name']}")
                    return True
                    
            print(f"Faculty member with ID {faculty_id} not found")
            return False
            
        except Exception as e:
            print(f"Error updating faculty member: {e}")
            return False
            
    def delete_faculty(self, faculty_id):
        """Delete faculty member"""
        try:
            for i, faculty in enumerate(self.faculty_data):
                if faculty['id'] == faculty_id:
                    deleted_faculty = self.faculty_data.pop(i)
                    self.save_data()
                    
                    print(f"Deleted faculty member: {deleted_faculty['name']}")
                    return True
                    
            print(f"Faculty member with ID {faculty_id} not found")
            return False
            
        except Exception as e:
            print(f"Error deleting faculty member: {e}")
            return False
            
    def get_faculty_by_id(self, faculty_id):
        """Get faculty member by ID"""
        for faculty in self.faculty_data:
            if faculty['id'] == faculty_id:
                return faculty
        return None
        
    def get_faculty_by_name(self, name):
        """Get faculty member by name"""
        for faculty in self.faculty_data:
            if faculty['name'].lower() == name.lower():
                return faculty
        return None
        
    def get_all_faculty(self):
        """Get all faculty members"""
        return self.faculty_data.copy()
        
    def search_faculty(self, query):
        """Search faculty members"""
        query = query.lower()
        results = []
        
        for faculty in self.faculty_data:
            if (query in faculty['name'].lower() or 
                query in faculty['department'].lower() or 
                query in faculty['email'].lower() or
                query in faculty.get('employee_id', '').lower()):
                results.append(faculty)
                
        return results
        
    def update_last_seen(self, faculty_name):
        """Update last seen timestamp for faculty member"""
        try:
            for faculty in self.faculty_data:
                if faculty['name'].lower() == faculty_name.lower():
                    faculty['last_seen'] = datetime.now().isoformat()
                    self.save_data()
                    return True
            return False
            
        except Exception as e:
            print(f"Error updating last seen for {faculty_name}: {e}")
            return False
            
    def get_faculty_count(self):
        """Get total number of faculty members"""
        return len(self.faculty_data)
        
    def get_active_faculty_count(self):
        """Get number of active faculty members"""
        return len([f for f in self.faculty_data if f.get('status', 'Active') == 'Active'])
        
    def export_faculty_data(self, file_path):
        """Export faculty data to file"""
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'w') as f:
                    json.dump(self.faculty_data, f, indent=2)
            elif file_path.endswith('.csv'):
                import csv
                with open(file_path, 'w', newline='') as f:
                    if self.faculty_data:
                        fieldnames = self.faculty_data[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.faculty_data)
                        
            print(f"Faculty data exported to {file_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting faculty data: {e}")
            return False
