# ModularGrid Price Monitor - Notification System Design

## Overview
This document outlines the notification system for alerting users when good deals are found on the ModularGrid marketplace.

## Notification Types

### 1. Windows System Notifications
- **Purpose**: Immediate alerts when the application is running
- **Implementation**: Using Windows toast notifications
- **Content**:
  - Module name and manufacturer
  - Current price and percentage below average
  - Brief condition summary
  - Action button to view listing

### 2. Email Notifications
- **Purpose**: Alerts when the user is not actively using the computer
- **Implementation**: SMTP client using user's email provider
- **Content**:
  - Subject: "Good Deal Alert: [Module Name]"
  - Body:
    - Module details (name, manufacturer, HP)
    - Price information (current price, average price, savings)
    - Condition description
    - Seller information and region
    - Direct link to listing
    - Timestamp of when deal was found

### 3. In-App Notifications
- **Purpose**: Persistent record of all detected deals
- **Implementation**: Notification center within the application UI
- **Features**:
  - Sortable list of all detected deals
  - Read/unread status
  - Ability to dismiss or save notifications
  - Filter by module type, price range, etc.

## Notification Settings

### User Configurable Options
- **Notification channels**: Enable/disable Windows notifications, emails
- **Notification frequency**: Immediate, hourly digest, daily digest
- **Threshold customization**:
  - Global threshold (e.g., 15% below average)
  - Per-module thresholds
  - Absolute price limits
- **Quiet hours**: Time periods when notifications are suppressed
- **Region filtering**: Only notify for listings in specific regions

## Notification Logic

### Deal Detection Algorithm
1. For each new or updated listing:
   - Calculate average historical price for the module
   - Determine percentage below average
   - Check if below global or module-specific threshold
   - Verify within user's region preferences
   - Check if price is below absolute maximum (if set)

2. If conditions are met:
   - Create new entry in Deals table
   - Generate appropriate notifications based on user settings
   - Update notification status in database

### Duplicate Prevention
- Track previously notified deals in database
- Use listing ID as unique identifier
- Only notify once per listing unless price changes significantly

## Implementation Details

### Windows Notifications
```python
from win10toast import ToastNotifier

def send_windows_notification(module_name, price, avg_price, percent_below, listing_url):
    toaster = ToastNotifier()
    title = f"Deal Alert: {module_name}"
    message = f"Price: ${price:.2f} (${avg_price:.2f} avg, {percent_below:.1f}% below)"
    toaster.show_toast(
        title,
        message,
        duration=10,
        icon_path="app_icon.ico",
        callback_on_click=lambda: open_url(listing_url)
    )
```

### Email Notifications
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(user_email, module_data, listing_data):
    # Email configuration from user preferences
    email_config = get_email_config()
    
    # Create message
    msg = MIMEMultipart()
    msg['Subject'] = f"ModularGrid Deal Alert: {module_data['name']}"
    msg['From'] = email_config['from_address']
    msg['To'] = user_email
    
    # Email body
    body = f"""
    Good deal found on ModularGrid!
    
    Module: {module_data['manufacturer']} {module_data['name']}
    Price: {listing_data['currency']} {listing_data['price']:.2f}
    Average Price: {listing_data['currency']} {listing_data['avg_price']:.2f}
    Savings: {listing_data['percent_below']:.1f}% below average
    
    Condition: {listing_data['condition']}
    Seller: {listing_data['seller']} ({listing_data['region']})
    
    View listing: {listing_data['url']}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.starttls()
        server.login(email_config['username'], email_config['password'])
        server.send_message(msg)
```

## User Experience Considerations

- **Notification fatigue**: Implement cooldown periods to prevent too many notifications
- **Relevance filtering**: Allow users to set "must-have" criteria for notifications
- **Urgency levels**: Differentiate between good deals and exceptional deals
- **Accessibility**: Ensure notifications are accessible (high contrast, screen reader support)
- **Mobile sync**: Future feature to sync notifications to mobile devices
