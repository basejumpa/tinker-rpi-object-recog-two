#!/bin/bash
# Setup script for Raspberry Pi Object Recognition Application

set -e

echo "======================================"
echo "Raspberry Pi Object Recognition Setup"
echo "======================================"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "Warning: This script is designed for Raspberry Pi"
    echo "Continuing anyway..."
fi

# Update system
echo "Updating system packages..."
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-opencv \
    python3-picamera2 \
    python3-numpy \
    python3-pil \
    python3-venv \
    libopenblas-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libfontconfig1-dev \
    libcairo2-dev \
    libgdk-pixbuf-xlib-2.0-dev \
    libpango1.0-dev \
    libgtk-3-dev \
    libhdf5-dev \
    libimath-dev \
    libopenexr-dev \
    libgstreamer1.0-dev \
    espeak \
    espeak-ng \
    alsa-utils \
    portaudio19-dev \
    python3-pyaudio

# Create virtual environment for Python packages
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv --system-site-packages
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment and install packages
echo "Installing Python packages in virtual environment..."
if [ -f requirements.txt ]; then
    # Use virtual environment to avoid externally-managed-environment issues
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Try to install TensorFlow Lite Runtime from Google Coral repo
    echo "Attempting to install TensorFlow Lite Runtime..."
    pip install --index-url https://google-coral.github.io/py-repo/ tflite_runtime 2>/dev/null || \
    echo "  Note: TensorFlow Lite Runtime not available. Application will run in demo mode."
    echo "  For full object detection, manually install a compatible TFLite package."
    
    deactivate
    echo "Python packages installed successfully"
else
    echo "Warning: requirements.txt not found"
fi

# Create models directory
echo "Creating models directory..."
mkdir -p models

# Download TensorFlow Lite model and labels
echo "Downloading object detection model..."
source venv/bin/activate
python download_model.py
deactivate

# Configure audio for HDMI
echo "Configuring audio output..."
sudo amixer cset numid=3 2  # Force HDMI audio output

echo ""
echo "======================================"
echo "Setup complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or use the helper script:"
echo "  ./run.sh"
echo ""
echo "Make sure your camera and HDMI display are connected."
echo ""
