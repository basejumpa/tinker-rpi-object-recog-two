"""
Display Manager Module

Handles displaying video frames on the HDMI output using OpenCV.
Requires X11 display server to be running.
"""

import cv2
import numpy as np
import os


class DisplayManager:
    """Manages the display output to HDMI"""
    
    def __init__(self, width=1920, height=1080):
        """
        Initialize the display manager
        
        Args:
            width: Display width in pixels
            height: Display height in pixels
            
        Raises:
            RuntimeError: If X11 display is not available
        """
        self.width = width
        self.height = height
        self.window_name = "Object Recognition"
        
        # Verify X11 display is available
        if not os.environ.get('DISPLAY'):
            raise RuntimeError("No X11 DISPLAY environment variable set. Cannot create window.")
        
        try:
            # Create a named window
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            
            # Set window to fullscreen for HDMI output
            cv2.setWindowProperty(
                self.window_name,
                cv2.WND_PROP_FULLSCREEN,
                cv2.WINDOW_FULLSCREEN
            )
            print(f"Display window created: {width}x{height}")
        except Exception as e:
            raise RuntimeError(f"Failed to create OpenCV window: {e}")
        
    def show_frame(self, frame):
        """
        Display a frame on the HDMI output
        
        Args:
            frame: Image frame to display (numpy array)
        """
        # Resize frame to match display resolution
        if frame.shape[:2] != (self.height, self.width):
            display_frame = cv2.resize(frame, (self.width, self.height))
        else:
            display_frame = frame
            
        # Display the frame
        cv2.imshow(self.window_name, display_frame)
        
    def cleanup(self):
        """Clean up display resources"""
        cv2.destroyWindow(self.window_name)
