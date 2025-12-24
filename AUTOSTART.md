# Auto-Start Configuration

This guide explains how to configure the application to start automatically on boot.

## Using systemd (Recommended)

### 1. Copy the Service File

```bash
sudo cp object-recognition.service /etc/systemd/system/
```

### 2. Edit the Service File

Edit the service file to match your installation path:

```bash
sudo nano /etc/systemd/system/object-recognition.service
```

Update these lines if needed:
- `User=pi` - Change to your username
- `WorkingDirectory=/home/pi/tinker-rpi-object-recog-two` - Change to your installation path
- `ExecStart=/usr/bin/python3 /home/pi/tinker-rpi-object-recog-two/main.py` - Update path

### 3. Enable and Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable object-recognition.service

# Start the service now
sudo systemctl start object-recognition.service
```

### 4. Check Service Status

```bash
sudo systemctl status object-recognition.service
```

### 5. View Logs

```bash
# View recent logs
sudo journalctl -u object-recognition.service -n 50

# Follow logs in real-time
sudo journalctl -u object-recognition.service -f
```

### 6. Stop or Disable Service

```bash
# Stop the service
sudo systemctl stop object-recognition.service

# Disable auto-start
sudo systemctl disable object-recognition.service
```

## Using rc.local (Alternative)

If you prefer a simpler approach, add to `/etc/rc.local`:

```bash
sudo nano /etc/rc.local
```

Add before `exit 0`:

```bash
# Start object recognition app
cd /home/pi/tinker-rpi-object-recog-two
python3 main.py > /tmp/object-recognition.log 2>&1 &
```

## Using crontab (Alternative)

```bash
crontab -e
```

Add this line:

```
@reboot cd /home/pi/tinker-rpi-object-recog-two && python3 main.py > /tmp/object-recognition.log 2>&1
```

## Troubleshooting Auto-Start

### Display Issues

If the display doesn't work on auto-start, you may need to:

1. Set display environment variable:
```bash
export DISPLAY=:0
```

2. Delay the start to wait for X server:
```bash
# Add to service file under [Service]
ExecStartPre=/bin/sleep 10
```

### Permission Issues

Ensure the user has access to:
- Camera device (`/dev/video0`)
- Audio devices
- Display (X11)

Add user to required groups:
```bash
sudo usermod -a -G video,audio pi
```

### Check What's Running

```bash
# Check if service is running
ps aux | grep main.py

# Check system logs
dmesg | tail -50
```
