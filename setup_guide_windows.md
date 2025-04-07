# ModularGrid Price Monitor - Setup Guide for Windows

This guide will walk you through the process of setting up and using the ModularGrid Price Monitor tool on your Windows computer. This tool automatically monitors the ModularGrid marketplace for eurorack modules being sold at prices below their typical market value.

## System Requirements

- Windows 10 or 11
- Python 3.8 or higher
- Internet connection
- ModularGrid Unicorn account (for accessing price history)

## Installation

### Step 1: Install Python

If you don't already have Python installed on your computer:

1. Visit [python.org](https://www.python.org/downloads/windows/)
2. Download the latest Python installer (Python 3.10 or newer recommended)
3. Run the installer
4. **Important**: Check the box that says "Add Python to PATH" during installation
5. Click "Install Now"

### Step 2: Download the ModularGrid Price Monitor

1. Download the ModularGrid Price Monitor ZIP file
2. Extract the ZIP file to a location on your computer (e.g., `C:\ModularGridMonitor`)

### Step 3: Install Required Dependencies

1. Open Command Prompt (you can search for "cmd" in the Windows search bar)
2. Navigate to the ModularGrid Price Monitor directory:
   ```
   cd C:\ModularGridMonitor
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

### Step 1: Create Configuration File

1. In the ModularGrid Price Monitor directory, locate the file named `config_template.json`
2. Make a copy of this file and rename it to `config.json`
3. Open `config.json` in a text editor (like Notepad)
4. Update the configuration with your information:

```json
{
    "username": "your_modulargrid_username",
    "password": "your_modulargrid_password",
    "scan_interval": 3600,
    "regions": ["EU", "USA", "Canada", "Australia", "Asia", "Africa", "South America"],
    "default_threshold": 15.0,
    "email_enabled": false,
    "email_address": "",
    "smtp_server": "",
    "smtp_port": 587,
    "smtp_username": "",
    "smtp_password": "",
    "from_address": "",
    "windows_enabled": true,
    "notification_frequency": "immediate",
    "quiet_hours_enabled": false,
    "quiet_hours_start": "22:00",
    "quiet_hours_end": "08:00"
}
```

### Step 2: Configure Your Settings

- `username` and `password`: Your ModularGrid login credentials
- `scan_interval`: How often to check for new listings (in seconds, default is 3600 = 1 hour)
- `regions`: Which regions to monitor (remove any regions you're not interested in)
- `default_threshold`: The percentage below average price that triggers an alert (default is 15.0%)
- `windows_enabled`: Set to `true` to receive Windows notifications
- `email_enabled`: Set to `true` if you want email notifications (requires additional email configuration)

### Step 3: Email Notification Setup (Optional)

If you want to receive email notifications:

1. Set `email_enabled` to `true`
2. Fill in your email address in `email_address`
3. Configure your email provider's SMTP settings:
   - For Gmail:
     - `smtp_server`: "smtp.gmail.com"
     - `smtp_port`: 587
     - `smtp_username`: Your Gmail address
     - `smtp_password`: Your app password (not your regular Gmail password)
     - `from_address`: Your Gmail address

   Note: For Gmail, you'll need to create an "App Password" in your Google Account settings.

## Using the ModularGrid Price Monitor

### Starting the Monitor

1. Open Command Prompt
2. Navigate to the ModularGrid Price Monitor directory:
   ```
   cd C:\ModularGridMonitor
   ```
3. Run the monitor:
   ```
   python modulargrid_monitor.py --monitor
   ```

The monitor will now run continuously, checking for new deals based on your configured scan interval.

### Running a Single Scan

If you just want to run a single scan without continuous monitoring:

```
python modulargrid_monitor.py --scan
```

### Adding Modules to Your Watchlist

The monitor will automatically track all modules listed on the marketplace, but you can set specific thresholds for modules you're particularly interested in:

1. Find the module ID from ModularGrid (it's in the URL when viewing a module, e.g., `https://modulargrid.net/e/modules/12345` has ID "12345")
2. Use the watchlist command:
   ```
   python modulargrid_monitor.py --add-to-watchlist 12345 --threshold 20 --max-price 300
   ```
   This will alert you when this module is listed at 20% below average price, but only if it's under €300.

### Viewing Your Watchlist

To see which modules you're currently watching:

```
python modulargrid_monitor.py --show-watchlist
```

### Removing Modules from Your Watchlist

To remove a module from your watchlist:

```
python modulargrid_monitor.py --remove-from-watchlist 12345
```

## Running Automatically at Startup

To have the ModularGrid Price Monitor start automatically when you turn on your computer:

1. Create a batch file (e.g., `start_monitor.bat`) in the ModularGrid Price Monitor directory with the following content:
   ```
   @echo off
   cd /d %~dp0
   python modulargrid_monitor.py --monitor
   ```

2. Press `Win + R`, type `shell:startup`, and press Enter
3. Copy a shortcut to your batch file into this folder

## Troubleshooting

### Authentication Issues

If you see "Authentication failed" errors:

1. Double-check your username and password in the config.json file
2. Make sure your Unicorn account is active
3. Try logging in manually on the ModularGrid website to confirm your credentials work

### No Notifications Appearing

If you're not receiving Windows notifications:

1. Check that `windows_enabled` is set to `true` in your config.json
2. Make sure Windows notifications are enabled in your system settings
3. Verify that the monitor is running (check the command prompt window)

### Email Notifications Not Working

If email notifications aren't being sent:

1. Confirm that `email_enabled` is set to `true`
2. Double-check your SMTP settings
3. For Gmail users, verify you're using an App Password, not your regular password
4. Check your spam folder

### Program Crashes or Errors

If the program crashes or shows error messages:

1. Check the log files in the ModularGrid Price Monitor directory
2. Make sure you have the latest version of Python and all dependencies
3. Try reinstalling the required packages:
   ```
   pip install -r requirements.txt --force-reinstall
   ```

### No Deals Found

If the monitor runs but never finds any deals:

1. Your threshold might be too high - try lowering the `default_threshold` value
2. There might not be any good deals at the moment - be patient!
3. Check that your regions are set correctly

## Support

If you encounter any issues not covered in this troubleshooting guide, please check the detailed log files in the ModularGrid Price Monitor directory. These logs contain valuable information that can help diagnose problems.

For additional help, please contact the developer with details about your issue and any relevant log files.
