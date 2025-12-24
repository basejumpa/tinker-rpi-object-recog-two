#!/usr/bin/env python3
"""
Download TensorFlow Lite model and labels for object detection

This script downloads the EfficientDet-Lite0 model and COCO labels
optimized for edge devices like Raspberry Pi.
"""

import os
import urllib.request
import sys


def download_file(url, destination):
    """Download a file from URL to destination"""
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"  Saved to {destination}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    """Download model and labels"""
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    print("Downloading TensorFlow Lite model and labels...")
    print()
    
    # EfficientDet-Lite0 model (optimized for edge devices)
    model_url = "https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip"
    model_zip = "models/model.zip"
    
    # Alternative: Use a pre-extracted model
    # This is a lightweight object detection model
    model_url = "https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/lite-model_efficientdet_lite0_detection_metadata_1.tflite"
    model_path = "models/efficientdet_lite0.tflite"
    
    # COCO labels
    labels_url = "https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip"
    
    # Download model
    success = download_file(model_url, model_path)
    
    if not success:
        print("\nFailed to download model. Trying alternative source...")
        # Try alternative source
        alt_model_url = "https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_coco_quant_postprocess.tflite"
        success = download_file(alt_model_url, model_path)
    
    # Create labels file
    labels_path = "models/coco_labels.txt"
    
    # COCO dataset labels
    coco_labels = [
        "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
        "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
        "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
        "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
        "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
        "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
        "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
        "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
        "toothbrush"
    ]
    
    print(f"\nCreating labels file: {labels_path}")
    with open(labels_path, "w") as f:
        for label in coco_labels:
            f.write(label + "\n")
    print(f"  Created {labels_path} with {len(coco_labels)} labels")
    
    print("\n" + "="*50)
    if success:
        print("Download complete!")
        print(f"Model: {model_path}")
        print(f"Labels: {labels_path}")
    else:
        print("Warning: Model download failed!")
        print("You may need to download the model manually.")
        print("\nRecommended model:")
        print("  https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1")
        print("\nPlace it at: models/efficientdet_lite0.tflite")
        sys.exit(1)
    print("="*50)


if __name__ == "__main__":
    main()
