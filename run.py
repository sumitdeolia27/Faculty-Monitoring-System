#!/usr/bin/env python3
"""
Faculty Presence Monitoring & Alert System
Main entry point for the application
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'cv2',
        'numpy', 
        'PIL',
        'ultralytics',
        'face_recognition'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        error_msg = f"""
Missing required packages: {', '.join(missing_packages)}

Please install them using:
pip install opencv-python numpy Pillow ultralytics face-recognition dlib

Note: You may need to install additional system dependencies for dlib and face_recognition.
        """
        print(error_msg)
        
        # Show GUI error if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", error_msg)
            root.destroy()
        except:
            pass
            
        return False
    
    return True

def main():
    """Main function to start the application"""
    print("Faculty Presence Monitoring & Alert System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("Please install missing dependencies and try again.")
        sys.exit(1)
    
    try:
        # Import main application
        from main import main as run_app
        
        print("Starting application...")
        run_app()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        error_msg = f"Error starting application: {e}"
        print(error_msg)
        
        # Show GUI error if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            pass
            
        sys.exit(1)

if __name__ == "__main__":
    main()
