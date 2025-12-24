"""
Object Detection Module using TensorFlow Lite

This module handles object detection using a TensorFlow Lite model,
optimized for Raspberry Pi.
"""

import numpy as np
import cv2

try:
    from tflite_runtime.interpreter import Interpreter
    TFLITE_AVAILABLE = True
except ImportError:
    try:
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter
        TFLITE_AVAILABLE = True
    except ImportError:
        print("Warning: Neither tflite_runtime nor tensorflow is available.")
        print("Object detection will run in demo mode without actual inference.")
        print("To enable object detection, install one of:")
        print("  1. pip install --index-url https://google-coral.github.io/py-repo/ tflite_runtime")
        print("  2. pip install tensorflow")
        TFLITE_AVAILABLE = False
        Interpreter = None


class ObjectDetector:
    """Object detector using TensorFlow Lite"""
    
    def __init__(self, model_path, labels_path, threshold=0.5):
        """
        Initialize the object detector
        
        Args:
            model_path: Path to the TFLite model file
            labels_path: Path to the labels file
            threshold: Confidence threshold for detections
        """
        self.threshold = threshold
        self.labels = self.load_labels(labels_path)
        
        # Check if TFLite is available
        if not TFLITE_AVAILABLE or Interpreter is None:
            print("Running in DEMO MODE - no actual object detection")
            self.interpreter = None
            self.height = 300
            self.width = 300
            return
        
        # Load TFLite model
        try:
            self.interpreter = Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            # Get input shape
            self.input_shape = self.input_details[0]['shape']
            self.height = self.input_shape[1]
            self.width = self.input_shape[2]
            
            print(f"Model loaded successfully: {model_path}")
            print(f"Input shape: {self.input_shape}")
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            print("Running in dummy mode for testing")
            self.interpreter = None
            self.height = 300
            self.width = 300
            
    def load_labels(self, labels_path):
        """Load class labels from file"""
        try:
            with open(labels_path, 'r') as f:
                labels = [line.strip() for line in f.readlines()]
            # Some models have a placeholder or empty first label, skip it
            if labels and (labels[0] == '???' or not labels[0]):
                labels = labels[1:]
            return labels
        except FileNotFoundError:
            print(f"Warning: Labels file not found: {labels_path}")
            print("Using dummy labels")
            return [f"Object_{i}" for i in range(91)]  # COCO has 90 classes
            
    def preprocess_frame(self, frame):
        """Preprocess frame for model input"""
        # Resize to model input size
        resized = cv2.resize(frame, (self.width, self.height))
        
        # Convert to RGB if needed
        if len(resized.shape) == 2:
            resized = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        elif resized.shape[2] == 4:
            resized = cv2.cvtColor(resized, cv2.COLOR_BGRA2RGB)
            
        # Normalize based on model requirements
        input_data = np.expand_dims(resized, axis=0)
        
        # Check if model expects float input (0-1) or uint8 (0-255)
        if self.interpreter and self.input_details[0]['dtype'] == np.float32:
            input_data = (np.float32(input_data) - 127.5) / 127.5
            
        return input_data
        
    def detect(self, frame):
        """
        Detect objects in the frame
        
        Args:
            frame: Input image frame (numpy array)
            
        Returns:
            List of detections, each containing:
                - label: Object class name
                - score: Confidence score
                - bbox: Bounding box coordinates (x1, y1, x2, y2)
        """
        if self.interpreter is None:
            # Dummy mode for testing
            return []
            
        original_height, original_width = frame.shape[:2]
        
        # Preprocess frame
        input_data = self.preprocess_frame(frame)
        
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get output tensors
        # Different models have different output formats
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
        
        detections = []
        
        for i in range(len(scores)):
            if scores[i] >= self.threshold:
                # Get bounding box coordinates
                ymin, xmin, ymax, xmax = boxes[i]
                
                # Convert to pixel coordinates
                x1 = int(xmin * original_width)
                y1 = int(ymin * original_height)
                x2 = int(xmax * original_width)
                y2 = int(ymax * original_height)
                
                # Get class label
                class_id = int(classes[i])
                if class_id < len(self.labels):
                    label = self.labels[class_id]
                else:
                    label = f"Unknown_{class_id}"
                    
                detections.append({
                    'label': label,
                    'score': float(scores[i]),
                    'bbox': (x1, y1, x2, y2)
                })
                
        return detections
