#!/usr/bin/env python3
"""
Faculty Presence Monitoring & Alert System
Main entry point for the application
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import FacultyMonitoringSystem
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure all required packages are installed:")
    print("pip install opencv-python numpy Pillow")
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import cv2
        import numpy as np
        from PIL import Image
        return True
    except ImportError as e:
        messagebox.showerror(
            "Missing Dependencies", 
            f"Required package not found: {e}\n\n"
            "Please install required packages:\n"
            "pip install opencv-python numpy Pillow"
        )
        return False

def main():
    """Main function to start the application"""
    print("Starting Faculty Presence Monitoring & Alert System...")
    
    # Check dependencies
    if not check_dependencies():
        return
        
    try:
        # Create and run the application
        app = FacultyMonitoringSystem()
        print("Application initialized successfully")
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Application Error", f"Failed to start application:\n{e}")

if __name__ == "__main__":
    main()
