"""
Configuration settings for Raspberry Pi Object Recognition Application
"""

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Display settings
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080

# Object detection settings
MODEL_PATH = "models/efficientdet_lite0.tflite"
LABELS_PATH = "models/coco_labels.txt"
DETECTION_THRESHOLD = 0.5
MAX_DETECTIONS = 10

# Text-to-Speech settings
TTS_RATE = 150  # Words per minute
TTS_VOLUME = 0.9  # Volume (0.0 to 1.0)

# Object tracking settings
OBJECT_COOLDOWN_SECONDS = 5  # Don't announce same object within this time
