#!/usr/bin/env python3
"""
Raspberry Pi Object Recognition Application

This application streams video from a PiCamera2, detects objects in real-time,
displays bounding boxes on an HDMI-connected TV, and announces detected objects
via text-to-speech through HDMI audio.

Author: basejumpa
License: MIT
"""

import sys
import time
import threading
from datetime import datetime, timedelta
from collections import defaultdict

import cv2
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import pyttsx3

import config
from object_detector import ObjectDetector
from display_manager import DisplayManager


class ObjectRecognitionApp:
    """Main application class for object recognition and display"""
    
    def __init__(self):
        """Initialize the application components"""
        print("Initializing Raspberry Pi Object Recognition Application...")
        
        # Initialize components
        self.camera = None
        self.detector = None
        self.display = None
        self.tts_engine = None
        
        # Object tracking for TTS
        self.detected_objects = defaultdict(lambda: datetime.min)
        self.tts_queue = []
        self.tts_lock = threading.Lock()
        self.running = False
        
    def initialize_camera(self):
        """Initialize the PiCamera2"""
        print("Initializing camera...")
        self.camera = Picamera2()
        
        # Configure camera
        camera_config = self.camera.create_preview_configuration(
            main={"size": (config.CAMERA_WIDTH, config.CAMERA_HEIGHT), "format": "RGB888"},
            controls={"FrameRate": config.CAMERA_FPS}
        )
        self.camera.configure(camera_config)
        self.camera.start()
        
        # Allow camera to warm up
        time.sleep(2)
        print("Camera initialized successfully")
        
    def initialize_detector(self):
        """Initialize the object detector"""
        print("Initializing object detector...")
        self.detector = ObjectDetector(
            model_path=config.MODEL_PATH,
            labels_path=config.LABELS_PATH,
            threshold=config.DETECTION_THRESHOLD
        )
        print("Object detector initialized successfully")
        
    def initialize_display(self):
        """Initialize the display manager for HDMI output"""
        print("Initializing display...")
        self.display = DisplayManager(
            width=config.DISPLAY_WIDTH,
            height=config.DISPLAY_HEIGHT
        )
        print("Display initialized successfully")
        
    def initialize_tts(self):
        """Initialize text-to-speech engine"""
        print("Initializing text-to-speech...")
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', config.TTS_RATE)
        self.tts_engine.setProperty('volume', config.TTS_VOLUME)
        print("Text-to-speech initialized successfully")
        
    def tts_worker(self):
        """Background worker thread for text-to-speech"""
        while self.running:
            text = None
            with self.tts_lock:
                if self.tts_queue:
                    text = self.tts_queue.pop(0)
            
            if text:
                print(f"Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                time.sleep(0.1)
                
    def announce_object(self, object_name):
        """Add object to TTS queue if it's new or cooldown expired"""
        current_time = datetime.now()
        last_announced = self.detected_objects[object_name]
        
        # Check if enough time has passed since last announcement
        if current_time - last_announced > timedelta(seconds=config.OBJECT_COOLDOWN_SECONDS):
            self.detected_objects[object_name] = current_time
            with self.tts_lock:
                self.tts_queue.append(object_name)
                
    def process_frame(self, frame):
        """Process a single frame: detect objects and draw bounding boxes"""
        # Detect objects
        detections = self.detector.detect(frame)
        
        # Process detections
        for detection in detections:
            label = detection['label']
            score = detection['score']
            bbox = detection['bbox']
            
            # Announce new objects
            self.announce_object(label)
            
            # Draw bounding box and label
            x1, y1, x2, y2 = bbox
            color = (0, 255, 0)  # Green
            thickness = 2
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # Draw label with background
            label_text = f"{label}: {score:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_thickness = 2
            
            (text_width, text_height), baseline = cv2.getTextSize(
                label_text, font, font_scale, font_thickness
            )
            
            # Draw background rectangle for text
            cv2.rectangle(
                frame,
                (x1, y1 - text_height - baseline - 5),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Draw text
            cv2.putText(
                frame,
                label_text,
                (x1, y1 - baseline - 5),
                font,
                font_scale,
                (0, 0, 0),  # Black text
                font_thickness
            )
        
        return frame
        
    def run(self):
        """Main application loop"""
        try:
            # Initialize all components
            self.initialize_camera()
            self.initialize_detector()
            self.initialize_display()
            self.initialize_tts()
            
            # Start TTS worker thread
            self.running = True
            tts_thread = threading.Thread(target=self.tts_worker, daemon=True)
            tts_thread.start()
            
            print("\nApplication started successfully!")
            print("Press Ctrl+C to exit\n")
            
            # Main processing loop
            while True:
                # Capture frame from camera
                frame = self.camera.capture_array()
                
                # Process frame (detect objects and draw)
                processed_frame = self.process_frame(frame)
                
                # Display frame on HDMI
                self.display.show_frame(processed_frame)
                
                # Check for exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up resources...")
        self.running = False
        
        if self.camera:
            self.camera.stop()
            
        if self.display:
            self.display.cleanup()
            
        cv2.destroyAllWindows()
        print("Cleanup complete")


def main():
    """Entry point for the application"""
    app = ObjectRecognitionApp()
    app.run()


if __name__ == "__main__":
    main()
