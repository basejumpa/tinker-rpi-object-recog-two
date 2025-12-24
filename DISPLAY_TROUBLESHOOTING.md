# Display and X11 Troubleshooting Guide

## The Issue: No Video Display on HDMI

If you see a text console on your HDMI TV instead of the video stream, it means the application cannot access the display system.

## Root Cause

The application uses **OpenCV's GUI functions** (`cv2.imshow()`) which require an **X11 desktop environment**. When you run the application from:
- SSH session to a text console
- TTY console (Ctrl+Alt+F1-F6)
- Systemd service without X11

...the application cannot create a display window and will fail.

## Solution: Run from Desktop Environment

### Best Solution: Use Raspberry Pi OS Desktop

1. **Install Desktop Environment** (if not already installed):
   ```bash
   sudo apt-get update
   sudo apt-get install raspberrypi-ui-mods
   ```

2. **Boot to Desktop**:
   ```bash
   sudo raspi-config
   # Navigate to: System Options → Boot / Auto Login
   # Select: Desktop / Desktop Autologin
   ```

3. **Reboot**:
   ```bash
   sudo reboot
   ```

4. **Run from Desktop Terminal**:
   - After reboot, you'll see the desktop on HDMI
   - Open Terminal (icon on desktop or menu)
   - Navigate to the project:
     ```bash
     cd ~/tinker-rpi-object-recog-two
     ```
   - Run the application:
     ```bash
     ./run.sh
     ```

### Alternative: Use VNC (Remote Desktop)

1. **Enable VNC Server**:
   ```bash
   sudo raspi-config
   # Navigate to: Interface Options → VNC → Yes
   sudo reboot
   ```

2. **Connect with VNC Client**:
   - Download RealVNC Viewer on your computer
   - Connect to `raspberrypi.local` or your Pi's IP address
   - Login with your Pi credentials

3. **Run from VNC Terminal**:
   - In the VNC session, open Terminal
   - Run the application

### For Advanced Users: Framebuffer (Future Enhancement)

Currently, the application uses OpenCV's highgui which requires X11. For true headless operation, the application would need to be modified to:
- Use framebuffer directly (`/dev/fb0`)
- Use DRM/KMS for direct HDMI output
- Use a different rendering backend

This is not currently implemented.

## Checking Your Environment

### Check if X11 is Available

```bash
echo $DISPLAY
```

**Expected output when X11 is available**: `:0` or `:1` or similar  
**Problem if output is**: (empty) - means no X11 display

### Check if Desktop is Running

```bash
ps aux | grep -i x11
```

Should show X11 or Xorg processes if desktop is running.

### Check if Running in Text Console

```bash
tty
```

**Output like** `/dev/tty1` - you're in text console (won't work)  
**Output like** `/dev/pts/0` - you're in desktop terminal (will work)

## Common Scenarios

### Scenario 1: SSH from Another Computer

**Problem**: SSH gives you a text console, not desktop access.

**Solution**: Use VNC or connect directly to the Pi's desktop.

### Scenario 2: Text Console on HDMI

**Problem**: Raspberry Pi is showing login prompt on HDMI.

**Solution**: 
1. Login to the text console
2. Run `startx` to start desktop, OR
3. Configure boot to desktop (see above)

### Scenario 3: Running as Systemd Service

**Problem**: Service starts but no display appears.

**Solution**: Systemd services don't have X11 access by default. You need to:
1. Run the service as the user with desktop access
2. Set proper DISPLAY and XAUTHORITY environment variables
3. Or start the application manually from desktop instead

## Testing Your Setup

### Minimal Test: Check OpenCV Window Creation

Create a test file `test_display.py`:

```python
#!/usr/bin/env python3
import cv2
import numpy as np
import os

print(f"DISPLAY environment: {os.environ.get('DISPLAY', 'NOT SET')}")

try:
    # Create a test image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "Test Display", (50, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    
    # Try to display it
    cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
    cv2.imshow("Test", img)
    
    print("SUCCESS: Window created! Press any key...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Test passed!")
    
except Exception as e:
    print(f"FAILED: {e}")
    print("\nYou need to run from a desktop environment!")
```

Run it:
```bash
source venv/bin/activate
python test_display.py
```

If this fails, your environment doesn't support GUI applications.

## Quick Reference

| Scenario | DISPLAY Variable | Will Work? |
|----------|------------------|------------|
| Desktop terminal | `:0` | ✅ Yes |
| VNC session | `:0` or `:1` | ✅ Yes |
| SSH (no X11) | (empty) | ❌ No |
| SSH with -X | `localhost:10.0` | ⚠️ Maybe (slow) |
| Text console | (empty) | ❌ No |
| Systemd service | (empty) | ❌ No (needs config) |

## Getting Help

If you still have issues:

1. Run the test script above and share output
2. Check: `echo $DISPLAY`
3. Check: `tty`
4. Check: `ps aux | grep -i x11`
5. Share all outputs for debugging
