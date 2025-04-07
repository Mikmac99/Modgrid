# ModularGrid Price Monitor - GUI User Manual

## Introduction

The ModularGrid Price Monitor is a powerful tool designed for eurorack enthusiasts who want to find great deals on modules. This graphical user interface (GUI) version provides an easy-to-use application that automatically monitors the ModularGrid marketplace for modules being sold below their typical market value and notifies you when good deals are found.

## Features

- **User-Friendly Interface**: Simple dashboard with all controls in one place
- **Automated Monitoring**: Continuously scans the ModularGrid marketplace for new listings
- **Price Analysis**: Compares current prices with historical data to identify good deals
- **Customizable Alerts**: Set your own thresholds for what constitutes a "good deal"
- **Multiple Notification Methods**: Receive alerts via Windows notifications or email
- **Region Filtering**: Focus on specific regions you're interested in
- **Watchlist**: Track specific modules you're looking to purchase
- **Quiet Hours**: Pause notifications during specified hours

## Main Interface

The ModularGrid Price Monitor has a simple interface with the following components:

### Dashboard Tab
- **Status Panel**: Shows current monitoring status, last scan time, next scan time, and deals found
- **Action Buttons**: Run Single Scan, Start/Stop Monitoring, View Deals
- **Activity Log**: Displays recent activity and notifications

### Logs Tab
- **Log Viewer**: Shows detailed application logs for troubleshooting

## Getting Started

### First Launch
1. Double-click the `ModularGridPriceMonitor.exe` file
2. The application will start and show the dashboard
3. Go to Settings > Account Settings to enter your ModularGrid credentials

### Setting Up Your Account
1. Go to Settings > Account Settings
2. Enter your ModularGrid username and password
3. Click Save
4. The application will automatically test your login credentials

## Basic Usage

### Running a Single Scan
1. Click the "Run Single Scan" button on the dashboard
2. Wait for the scan to complete
3. Check the "Deals Found" counter and activity log for results

### Starting Continuous Monitoring
1. Click the "Start Monitoring" button on the dashboard
2. The application will run scans at the configured interval
3. You'll receive notifications when deals are found
4. Click "Stop Monitoring" to pause the process

### Viewing Deals
1. Click the "View Deals" button on the dashboard
2. A window will open showing all current deals
3. Click "Open in Browser" to view a listing on ModularGrid

### Managing Your Watchlist
1. Go to Tools > Manage Watchlist
2. Add modules you're interested in with custom thresholds
3. Remove modules you're no longer interested in

## Configuration Options

### Account Settings
- **ModularGrid Username**: Your ModularGrid account username
- **ModularGrid Password**: Your ModularGrid account password

### Notification Settings
- **Windows Notifications**: Enable/disable Windows notifications
- **Email Notifications**: Enable/disable email notifications
- **Email Settings**: Configure your email server settings
- **Notification Frequency**: Choose between immediate or digest notifications
- **Quiet Hours**: Set hours during which notifications are suppressed

### General Settings
- **Scan Interval**: How often to check for new listings (in seconds)
- **Default Threshold**: The percentage below average price that triggers an alert
- **Regions**: Which regions to monitor for listings

## Menu Options

### File Menu
- **Run Single Scan**: Perform a one-time scan of the marketplace
- **Start Monitoring**: Begin continuous monitoring
- **Stop Monitoring**: Pause continuous monitoring
- **Exit**: Close the application

### Tools Menu
- **Manage Watchlist**: Add or remove modules from your watchlist
- **View Deals**: See all deals that have been found
- **Clear Logs**: Clear the log display

### Settings Menu
- **Account Settings**: Configure your ModularGrid login credentials
- **Notification Settings**: Configure how you receive alerts
- **General Settings**: Adjust scan intervals, thresholds, and regions

### Help Menu
- **User Manual**: View this user manual
- **About**: Information about the application

## Troubleshooting

### Login Issues
If you see "Login Failed" in the status:
- Double-check your username and password
- Ensure your Unicorn account is active
- Check your internet connection

### No Deals Found
If the monitor runs but never finds deals:
- Your threshold might be too high - try lowering it
- There might not be any good deals at the moment
- Check that you've selected appropriate regions

### Notification Problems
If you're not receiving notifications:
- Check that notifications are enabled in settings
- For email notifications, verify your email server settings
- For Windows notifications, check your Windows notification settings

### Application Crashes
If the application crashes:
- Check the log files in the application directory
- Make sure your Windows is up to date
- Try running the application as administrator

## Tips for Best Results

- Set a reasonable scan interval (1 hour is recommended)
- Add specific modules to your watchlist with custom thresholds
- Use email notifications for important deals you don't want to miss
- Configure quiet hours to avoid being disturbed at night
- Regularly check the "View Deals" section as some deals may sell quickly

## Privacy and Security

Your ModularGrid credentials are stored locally on your computer and are only used to authenticate with the ModularGrid website. The application does not share your information with any third parties.

For additional security:
- Store the application in a secure location on your computer
- Do not share your config.json file, as it contains your login credentials
