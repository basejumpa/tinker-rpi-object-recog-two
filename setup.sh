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

# Install Python packages
echo "Installing Python dependencies..."
pip3 install --upgrade pip --break-system-packages 2>/dev/null || pip3 install --upgrade pip

# Install requirements with system packages preferred
echo "Installing Python packages (using system packages where available)..."
if [ -f requirements.txt ]; then
    # Try with --break-system-packages first (needed for Debian Bookworm and newer)
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || \
    pip3 install -r requirements.txt
else
    echo "Warning: requirements.txt not found"
fi

# Create models directory
echo "Creating models directory..."
mkdir -p models

# Download TensorFlow Lite model and labels
echo "Downloading object detection model..."
python3 download_model.py

# Configure audio for HDMI
echo "Configuring audio output..."
sudo amixer cset numid=3 2  # Force HDMI audio output

echo ""
echo "======================================"
echo "Setup complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Make sure your camera and HDMI display are connected."
echo ""
