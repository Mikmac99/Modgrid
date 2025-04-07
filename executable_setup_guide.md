# ModularGrid Price Monitor - Executable Setup Guide

## Introduction

This guide will walk you through the process of setting up and using the ModularGrid Price Monitor executable on your Windows computer. This application automatically monitors the ModularGrid marketplace for eurorack modules being sold at prices below their typical market value.

## System Requirements

- Windows 10 or 11
- Internet connection
- ModularGrid Unicorn account (for accessing price history)

## Installation

### Step 1: Download the Application

1. Download the ModularGrid Price Monitor ZIP file
2. Extract the ZIP file to a location on your computer (e.g., `C:\ModularGridMonitor`)

### Step 2: Run the Application

1. Navigate to the folder where you extracted the files
2. Double-click on `ModularGridPriceMonitor.exe` to start the application
3. The application will start and show the main dashboard

That's it! No additional installation steps are required as the executable contains all necessary components.

## First-Time Setup

When you first run the application, you'll need to configure your ModularGrid account:

1. Go to **Settings > Account Settings**
2. Enter your ModularGrid username and password
3. Click **Save**
4. The application will automatically test your login credentials

## Using the Application

### Dashboard

The main dashboard shows:
- Current monitoring status
- Last scan time
- Next scheduled scan
- Number of deals found
- Recent activity log

### Running a Scan

You can run a scan in two ways:
- Click the **Run Single Scan** button for a one-time scan
- Click the **Start Monitoring** button for continuous monitoring

### Viewing Deals

To view deals that have been found:
1. Click the **View Deals** button on the dashboard
2. A window will open showing all current deals
3. Click **Open in Browser** to view a listing on ModularGrid

### Managing Your Watchlist

To add specific modules to your watchlist:
1. Go to **Tools > Manage Watchlist**
2. Click **Add Module**
3. Enter the module ID (found in the ModularGrid URL)
4. Set your desired threshold percentage and maximum price
5. Click **Add**

## Configuration Options

### Notification Settings

To configure notifications:
1. Go to **Settings > Notification Settings**
2. Enable/disable Windows notifications
3. Configure email notifications (optional)
4. Set quiet hours if desired

### General Settings

To adjust general settings:
1. Go to **Settings > General Settings**
2. Change the scan interval (in seconds)
3. Adjust the default threshold percentage
4. Select which regions to monitor

## Troubleshooting

### Application Won't Start

If the application doesn't start:
- Make sure you've extracted all files from the ZIP
- Try running as administrator
- Check your antivirus software isn't blocking the application

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

## Support

If you encounter any issues not covered in this guide, please check the detailed log files in the application directory. These logs contain valuable information that can help diagnose problems.
