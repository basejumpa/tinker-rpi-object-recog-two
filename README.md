# Raspberry Pi Object Recognition Application

A real-time object detection application for Raspberry Pi Zero 2W that streams video from PiCamera2, detects objects, displays bounding boxes on an HDMI-connected TV, and announces detected objects via text-to-speech.

## Features

- 🎥 Real-time video streaming from PiCamera2
- 🔍 Object detection using TensorFlow Lite (optimized for edge devices)
- 📺 Live video display with bounding boxes on HDMI-connected TV
- 🔊 Text-to-speech announcements of detected objects via HDMI audio
- ⚡ Optimized for Raspberry Pi Zero 2W
- 🎯 Smart object tracking (announces only new or re-detected objects)

## Hardware Requirements

- **Raspberry Pi Zero 2W** (or any Raspberry Pi model)
- **PiCamera2** (Raspberry Pi Camera Module)
- **TV or Monitor** connected via HDMI
- **MicroSD Card** (16GB+ recommended)
- **Power Supply** (5V, 2.5A recommended)

## Software Requirements

- **Raspberry Pi OS Lite Trixie** (or any recent Raspberry Pi OS)
- **Python 3.13** (or Python 3.9+)
- **Internet connection** (for initial setup and model download)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/basejumpa/tinker-rpi-object-recog-two.git
cd tinker-rpi-object-recog-two
```

### 2. Run Setup Script

The setup script will install all dependencies, download the object detection model, and configure the system:

```bash
./setup.sh
```

This script will:
- Install system dependencies optimized for Debian Trixie (OpenCV, PiCamera2, audio libraries, etc.)
- Install Python packages from `requirements.txt`
- Download the TensorFlow Lite object detection model
- Create necessary directories
- Configure HDMI audio output

**Note:** The setup script is optimized for Raspberry Pi OS Trixie and uses:
- System packages for major dependencies (python3-opencv, python3-picamera2, python3-numpy, python3-pil)
- A Python virtual environment for remaining packages to comply with PEP 668 (externally-managed-environment)

### 3. Manual Installation (Alternative)

If you prefer to install dependencies manually:

```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-opencv python3-picamera2 python3-numpy python3-pil python3-venv espeak alsa-utils

# Create virtual environment
python3 -m venv venv --system-site-packages

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Download the model
python download_model.py

# Deactivate virtual environment
deactivate

# Configure HDMI audio
sudo amixer cset numid=3 2
```

## Usage

### Basic Usage

Run the application using the helper script:

```bash
./run.sh
```

Or manually activate the virtual environment:

```bash
source venv/bin/activate
python main.py
```

The application will:
1. Initialize the camera
2. Start the object detector
3. Display live video on the HDMI output
4. Draw bounding boxes around detected objects
5. Announce detected objects via audio

### Stopping the Application

Press `Ctrl+C` to stop the application gracefully.

## Configuration

Edit `config.py` to customize the application behavior:

```python
# Camera settings
CAMERA_WIDTH = 640          # Camera capture width
CAMERA_HEIGHT = 480         # Camera capture height
CAMERA_FPS = 30             # Frames per second

# Display settings
DISPLAY_WIDTH = 1920        # HDMI output width
DISPLAY_HEIGHT = 1080       # HDMI output height

# Object detection
DETECTION_THRESHOLD = 0.5   # Confidence threshold (0.0 to 1.0)
MAX_DETECTIONS = 10         # Maximum objects to detect per frame

# Text-to-Speech
TTS_RATE = 150              # Words per minute
TTS_VOLUME = 0.9            # Volume (0.0 to 1.0)

# Object tracking
OBJECT_COOLDOWN_SECONDS = 5 # Time before re-announcing same object
```

## Architecture

The application consists of several modules:

- **`main.py`**: Main application entry point and orchestration
- **`object_detector.py`**: TensorFlow Lite object detection wrapper
- **`display_manager.py`**: HDMI display management
- **`config.py`**: Configuration settings
- **`download_model.py`**: Model download utility
- **`setup.sh`**: Automated setup script

### Object Detection Model

The application uses **EfficientDet-Lite0** or **MobileNet SSD**, optimized TensorFlow Lite models for edge devices. These models are:
- Lightweight and fast
- Designed for resource-constrained devices
- Trained on the COCO dataset (90 object classes)

### Detected Object Classes

The model can detect 80+ common objects including:
- People, vehicles (car, bicycle, motorcycle, bus, truck)
- Animals (dog, cat, bird, horse, etc.)
- Everyday objects (bottle, cup, book, phone, etc.)
- Furniture (chair, couch, bed, table)
- And many more...

See `models/coco_labels.txt` for the complete list after running setup.

## Troubleshooting

### Camera Not Working

```bash
# Check if camera is detected
vcgencmd get_camera

# Enable camera interface if needed
sudo raspi-config
# Navigate to: Interface Options -> Camera -> Enable
```

### No Audio Output

```bash
# Force HDMI audio output
sudo amixer cset numid=3 2

# Check audio devices
aplay -l

# Test audio
speaker-test -t wav -c 2
```

### Display Issues

```bash
# Check HDMI output
tvservice -s

# Force HDMI mode in /boot/config.txt
sudo nano /boot/config.txt
# Add or uncomment:
# hdmi_force_hotplug=1
# hdmi_drive=2
```

### Performance Issues

If the application runs slowly:
1. Reduce camera resolution in `config.py`
2. Increase `DETECTION_THRESHOLD` to reduce false positives
3. Reduce `MAX_DETECTIONS`
4. Consider using a more powerful Raspberry Pi model

### Model Download Fails

If automatic model download fails:
1. Manually download from: https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1
2. Place the file at `models/efficientdet_lite0.tflite`
3. Ensure `models/coco_labels.txt` exists

## Development

### Project Structure

```
tinker-rpi-object-recog-two/
├── main.py                 # Main application
├── object_detector.py      # Object detection module
├── display_manager.py      # Display management
├── config.py              # Configuration
├── download_model.py      # Model download utility
├── setup.sh              # Setup script
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── models/              # Model files (created during setup)
    ├── efficientdet_lite0.tflite
    └── coco_labels.txt
```

### Running on Development Machine

For testing on a non-Raspberry Pi system:
1. Install dependencies: `pip install -r requirements.txt`
2. The application will run in "dummy mode" if PiCamera2 is not available
3. Use a webcam or test video instead of PiCamera2

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

basejumpa

## Acknowledgments

- TensorFlow Lite for efficient edge inference
- Raspberry Pi Foundation for excellent hardware
- OpenCV for computer vision capabilities
- The open-source community