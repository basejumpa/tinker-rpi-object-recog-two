# TensorFlow Lite Installation Guide for Raspberry Pi

This document provides instructions for installing TensorFlow Lite on Raspberry Pi for object detection.

## The Challenge

TensorFlow Lite Runtime (`tflite-runtime`) is not consistently available on PyPI or piwheels for all ARM platforms and Python versions. This can cause installation issues.

## Installation Options

### Option 1: Google Coral Repository (Recommended for ARM)

Try installing from the Google Coral repository:

```bash
source venv/bin/activate
pip install --index-url https://google-coral.github.io/py-repo/ tflite_runtime
deactivate
```

This works for many ARM platforms but may not have builds for all Python versions.

### Option 2: Full TensorFlow Package

Install the full TensorFlow package (larger but more compatible):

```bash
source venv/bin/activate
pip install tensorflow
deactivate
```

**Note:** This is a much larger package (~400MB+) and may be slow on Raspberry Pi Zero 2W.

### Option 3: System Package (Debian/Ubuntu)

Some distributions provide TensorFlow Lite as a system package:

```bash
sudo apt-get update
sudo apt-get install python3-tflite-runtime
```

Then modify `object_detector.py` to import from system packages.

### Option 4: Build from Source

For advanced users, build TensorFlow Lite from source:

1. Follow instructions at: https://www.tensorflow.org/lite/guide/build_arm
2. This gives you the most control but takes considerable time

## Demo Mode

The application includes a **demo mode** that works without TensorFlow Lite:

- The camera and display will work normally
- Object detection will be disabled (no bounding boxes)
- Text-to-speech will not announce objects
- Useful for testing camera and display setup

To run in demo mode, simply run the application without TensorFlow Lite installed:

```bash
./run.sh
```

## Checking Installation

To verify TensorFlow Lite is installed:

```bash
source venv/bin/activate
python -c "from tflite_runtime.interpreter import Interpreter; print('TFLite Runtime: OK')" || \
python -c "import tensorflow as tf; print('TensorFlow: OK')"
deactivate
```

## Troubleshooting

### Error: "No matching distribution found for tflite-runtime"

This means tflite-runtime is not available for your platform/Python version.
- Try Option 1 (Google Coral repo)
- Or use Option 2 (full TensorFlow)
- Or run in demo mode

### Error: "ImportError: No module named 'tflite_runtime'"

TensorFlow Lite is not installed. Choose one of the installation options above.

### Application runs but no objects detected

- Check if the model file exists in `models/efficientdet_lite0.tflite`
- Run `python download_model.py` to download the model
- Check console output for error messages

### Model download fails

If the automatic model download fails:

1. Manually download a TFLite model:
   - EfficientDet Lite: https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1
   - MobileNet SSD: https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip

2. Place it in the `models/` directory as `efficientdet_lite0.tflite`

3. Ensure `models/coco_labels.txt` exists (created by setup script)

## Platform-Specific Notes

### Raspberry Pi Zero 2W (ARM64)

- Google Coral repo may work for older Python versions (3.9-3.11)
- For Python 3.13, you may need to use full TensorFlow or wait for updated builds
- Consider using Raspberry Pi OS Bullseye (Python 3.9) for better compatibility

### Raspberry Pi 4/5

Similar to Zero 2W but generally faster installation and execution.

## Performance Notes

- **TFLite Runtime**: Smallest, fastest, recommended
- **TensorFlow**: Larger but more compatible
- **Demo Mode**: No inference, just camera/display testing

## Getting Help

If you continue to have issues:

1. Check Python version: `python3 --version`
2. Check platform: `uname -m`
3. Try demo mode first to verify camera/display work
4. Share error messages for specific troubleshooting
