#!/usr/bin/env python3
"""
Test script to verify application structure without hardware dependencies
"""

import sys
import os

print("Testing application structure...")
print()

# Test 1: Check all files exist
print("1. Checking files exist...")
required_files = [
    'main.py',
    'config.py',
    'object_detector.py',
    'display_manager.py',
    'download_model.py',
    'setup.sh',
    'requirements.txt',
    'README.md'
]

all_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING")
        all_exist = False

if not all_exist:
    print("\nError: Some required files are missing!")
    sys.exit(1)

print("\n2. Checking Python syntax...")
for py_file in ['main.py', 'config.py', 'object_detector.py', 'display_manager.py', 'download_model.py']:
    try:
        with open(py_file, 'r') as f:
            compile(f.read(), py_file, 'exec')
        print(f"  ✓ {py_file} - syntax OK")
    except SyntaxError as e:
        print(f"  ✗ {py_file} - syntax error: {e}")
        sys.exit(1)

print("\n3. Checking configuration...")
try:
    import config
    required_attrs = [
        'CAMERA_WIDTH',
        'CAMERA_HEIGHT',
        'CAMERA_FPS',
        'DISPLAY_WIDTH',
        'DISPLAY_HEIGHT',
        'MODEL_PATH',
        'LABELS_PATH',
        'DETECTION_THRESHOLD'
    ]
    
    for attr in required_attrs:
        if hasattr(config, attr):
            print(f"  ✓ {attr} = {getattr(config, attr)}")
        else:
            print(f"  ✗ {attr} - MISSING")
            sys.exit(1)
            
except Exception as e:
    print(f"  ✗ Error importing config: {e}")
    sys.exit(1)

print("\n4. Checking module structure...")
modules = {
    'object_detector': ['ObjectDetector'],
    'display_manager': ['DisplayManager']
}

for module_name, expected_classes in modules.items():
    try:
        # Check if file contains expected class definitions
        with open(f"{module_name}.py", 'r') as f:
            content = f.read()
            for cls in expected_classes:
                if f"class {cls}" in content:
                    print(f"  ✓ {module_name}.{cls} - found")
                else:
                    print(f"  ✗ {module_name}.{cls} - NOT FOUND")
                    sys.exit(1)
    except Exception as e:
        print(f"  ✗ Error checking {module_name}: {e}")
        sys.exit(1)

print("\n" + "="*50)
print("✓ ALL TESTS PASSED!")
print("="*50)
print("\nThe application structure is valid.")
print("To run on Raspberry Pi:")
print("  1. Run ./setup.sh to install dependencies")
print("  2. Run python3 main.py to start the application")
print()
