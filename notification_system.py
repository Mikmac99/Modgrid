#!/usr/bin/env python3
"""
ModularGrid Price Monitor - Notification System
----------------------------------------------
This module handles notifications for the ModularGrid Price Monitor.
It includes functions to send Windows notifications, email alerts,
and manage notification preferences.
"""

import os
import logging
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("notifications.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("modulargrid_notifications")

class NotificationSystem:
    """Class to handle notifications for ModularGrid Price Monitor."""
    
    def __init__(self, database, config_file=None):
        """
        Initialize the notification system.
        
        Args:
            database: ModularGridDatabase instance
            config_file (str, optional): Path to configuration file
        """
        self.db = database
        self.config = {}
        
        # Load configuration if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Load from database preferences
            self._load_config_from_db()
    
    def _load_config_from_db(self):
        """Load notification configuration from database preferences."""
        try:
            # Email notification settings
            email_enabled = self.db.get_preference('email_notifications', 'false')
            self.config['email_enabled'] = email_enabled.lower() == 'true'
            
            self.config['email_address'] = self.db.get_preference('email_address', '')
            self.config['smtp_server'] = self.db.get_preference('smtp_server', '')
            self.config['smtp_port'] = int(self.db.get_preference('smtp_port', '587'))
            self.config['smtp_username'] = self.db.get_preference('smtp_username', '')
            self.config['smtp_password'] = self.db.get_preference('smtp_password', '')
            self.config['from_address'] = self.db.get_preference('from_address', '')
            
            # Windows notification settings
            win_enabled = self.db.get_preference('windows_notifications', 'true')
            self.config['windows_enabled'] = win_enabled.lower() == 'true'
            
            # Notification frequency
            self.config['notification_frequency'] = self.db.get_preference('notification_frequency', 'immediate')
            
            # Quiet hours
            self.config['quiet_hours_enabled'] = self.db.get_preference('quiet_hours_enabled', 'false').lower() == 'true'
            self.config['quiet_hours_start'] = self.db.get_preference('quiet_hours_start', '22:00')
            self.config['quiet_hours_end'] = self.db.get_preference('quiet_hours_end', '08:00')
            
            logger.info("Loaded notification configuration from database")
        except Exception as e:
            logger.error(f"Error loading notification configuration: {e}")
    
    def save_config_to_db(self):
        """Save notification configuration to database preferences."""
        try:
            # Email notification settings
            self.db.set_preference('email_notifications', str(self.config.get('email_enabled', False)).lower())
            self.db.set_preference('email_address', self.config.get('email_address', ''))
            self.db.set_preference('smtp_server', self.config.get('smtp_server', ''))
            self.db.set_preference('smtp_port', str(self.config.get('smtp_port', 587)))
            self.db.set_preference('smtp_username', self.config.get('smtp_username', ''))
            self.db.set_preference('smtp_password', self.config.get('smtp_password', ''))
            self.db.set_preference('from_address', self.config.get('from_address', ''))
            
            # Windows notification settings
            self.db.set_preference('windows_notifications', str(self.config.get('windows_enabled', True)).lower())
            
            # Notification frequency
            self.db.set_preference('notification_frequency', self.config.get('notification_frequency', 'immediate'))
            
            # Quiet hours
            self.db.set_preference('quiet_hours_enabled', str(self.config.get('quiet_hours_enabled', False)).lower())
            self.db.set_preference('quiet_hours_start', self.config.get('quiet_hours_start', '22:00'))
            self.db.set_preference('quiet_hours_end', self.config.get('quiet_hours_end', '08:00'))
            
            logger.info("Saved notification configuration to database")
            return True
        except Exception as e:
            logger.error(f"Error saving notification configuration: {e}")
            return False
    
    def is_in_quiet_hours(self):
        """
        Check if current time is within quiet hours.
        
        Returns:
            bool: True if in quiet hours, False otherwise
        """
        if not self.config.get('quiet_hours_enabled', False):
            return False
        
        try:
            now = datetime.now().time()
            start_str = self.config.get('quiet_hours_start', '22:00')
            end_str = self.config.get('quiet_hours_end', '08:00')
            
            start_time = datetime.strptime(start_str, '%H:%M').time()
            end_time = datetime.strptime(end_str, '%H:%M').time()
            
            # Handle overnight quiet hours
            if start_time > end_time:
                return now >= start_time or now <= end_time
            else:
                return start_time <= now <= end_time
        except Exception as e:
            logger.error(f"Error checking quiet hours: {e}")
            return False
    
    def should_send_notification(self, deal_id):
        """
        Check if a notification should be sent for a deal.
        
        Args:
            deal_id: Deal ID
            
        Returns:
            bool: True if notification should be sent, False otherwise
        """
        try:
            # Check if in quiet hours
            if self.is_in_quiet_hours():
                logger.info(f"In quiet hours, skipping notification for deal {deal_id}")
                return False
            
            # Check if already notified
            self.db.cursor.execute(
                "SELECT notified FROM Deals WHERE id = ?",
                (deal_id,)
            )
            result = self.db.cursor.fetchone()
            
            if result and result['notified']:
                logger.info(f"Already notified for deal {deal_id}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error checking notification status: {e}")
            return False
    
    def send_windows_notification(self, deal):
        """
        Send a Windows notification for a deal.
        
        Args:
            deal (dict): Deal information
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.config.get('windows_enabled', True):
            logger.info("Windows notifications are disabled")
            return False
        
        try:
            # Import here to avoid dependency issues on non-Windows platforms
            from win10toast import ToastNotifier
            
            module_name = deal.get('module_name', '')
            manufacturer = deal.get('manufacturer', '')
            price = deal.get('current_price', 0)
            currency = deal.get('currency', 'EUR')
            avg_price = deal.get('avg_price', 0)
            percent_below = deal.get('percent_below', 0)
            
            title = f"ModularGrid Deal Alert: {manufacturer} {module_name}"
            message = f"Price: {currency} {price:.2f} ({percent_below:.1f}% below average)\n"
            message += f"Average price: {currency} {avg_price:.2f}\n"
            message += f"Seller: {deal.get('seller', '')} ({deal.get('region', '')})"
            
            toaster = ToastNotifier()
            toaster.show_toast(
                title,
                message,
                duration=10,
                icon_path=os.path.join(os.path.dirname(__file__), "icon.ico"),
                threaded=True
            )
            
            logger.info(f"Sent Windows notification for {module_name}")
            return True
        except ImportError:
            logger.error("win10toast module not found. Windows notifications are not available.")
            return False
        except Exception as e:
            logger.error(f"Error sending Windows notification: {e}")
            return False
    
    def send_email_notification(self, deal):
        """
        Send an email notification for a deal.
        
        Args:
            deal (dict): Deal information
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.config.get('email_enabled', False):
            logger.info("Email notifications are disabled")
            return False
        
        email_address = self.config.get('email_address')
        if not email_address:
            logger.error("No email address configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            
            module_name = deal.get('module_name', '')
            manufacturer = deal.get('manufacturer', '')
            
            msg['Subject'] = f"ModularGrid Deal Alert: {manufacturer} {module_name}"
            msg['From'] = self.config.get('from_address', self.config.get('smtp_username', ''))
            msg['To'] = email_address
            
            # Email body
            price = deal.get('current_price', 0)
            currency = deal.get('currency', 'EUR')
            avg_price = deal.get('avg_price', 0)
            percent_below = deal.get('percent_below', 0)
            price_diff = deal.get('price_difference', 0)
            
            body = f"""
            Good deal found on ModularGrid!
            
            Module: {manufacturer} {module_name}
            Price: {currency} {price:.2f}
            Average Price: {currency} {avg_price:.2f}
            Savings: {currency} {price_diff:.2f} ({percent_below:.1f}% below average)
            
            Condition: {deal.get('condition', 'Not specified')}
            Seller: {deal.get('seller', 'Unknown')} ({deal.get('region', 'Unknown')})
            
            View listing: {deal.get('url', '')}
            
            ---
            This is an automated notification from your ModularGrid Price Monitor.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            smtp_server = self.config.get('smtp_server', '')
            smtp_port = self.config.get('smtp_port', 587)
            username = self.config.get('smtp_username', '')
            password = self.config.get('smtp_password', '')
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                if username and password:
                    server.login(username, password)
                server.send_message(msg)
            
            logger.info(f"Sent email notification for {module_name} to {email_address}")
            return True
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    def notify_deal(self, deal):
        """
        Send notifications for a deal using all enabled methods.
        
        Args:
            deal (dict): Deal information
            
        Returns:
            bool: True if any notification was sent, False otherwise
        """
        deal_id = deal.get('id')
        
        if not self.should_send_notification(deal_id):
            return False
        
        notifications_sent = False
        
        # Send Windows notification
        if self.config.get('windows_enabled', True):
            win_sent = self.send_windows_notification(deal)
            notifications_sent = notifications_sent or win_sent
        
        # Send email notification
        if self.config.get('email_enabled', False):
            email_sent = self.send_email_notification(deal)
            notifications_sent = notifications_sent or email_sent
        
        # Mark deal as notified
        if notifications_sent:
            self.db.mark_deal_notified(deal_id)
        
        return notifications_sent
    
    def notify_deals(self, deals):
        """
        Send notifications for multiple deals.
        
        Args:
            deals (list): List of deal information
            
        Returns:
            int: Number of deals notified
        """
        if not deals:
            logger.info("No deals to notify")
            return 0
        
        # Check notification frequency
        frequency = self.config.get('notification_frequency', 'immediate')
        
        if frequency == 'immediate':
            # Send individual notifications for each deal
            count = 0
            for deal in deals:
                if self.notify_deal(deal):
                    count += 1
            return count
        elif frequency == 'digest':
            # Send a single digest notification for all deals
            return self._send_digest_notification(deals)
        else:
            logger.warning(f"Unknown notification frequency: {frequency}")
            return 0
    
    def _send_digest_notification(self, deals):
        """
        Send a digest notification for multiple deals.
        
        Args:
            deals (list): List of deal information
            
        Returns:
            int: Number of deals included in the digest
        """
        if not deals:
            return 0
        
        try:
            # Windows notification (simple summary)
            if self.config.get('windows_enabled', True):
                try:
                    from win10toast import ToastNotifier
                    
                    title = f"ModularGrid Deal Alert: {len(deals)} new deals found!"
                    message = "Open the app to see details."
                    
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        title,
                        message,
                        duration=10,
                        icon_path=os.path.join(os.path.dirname(__file__), "icon.ico"),
                        threaded=True
                    )
                except ImportError:
                    logger.error("win10toast module not found. Windows notifications are not available.")
            
            # Email notification (detailed digest)
            if self.config.get('email_enabled', False):
                email_address = self.config.get('email_address')
                if email_address:
                    # Create message
                    msg = MIMEMultipart()
                    
                    msg['Subject'] = f"ModularGrid Deal Digest: {len(deals)} new deals found!"
                    msg['From'] = self.config.get('from_address', self.config.get('smtp_username', ''))
                    msg['To'] = email_address
                    
                    # Email body
                    body = "The following good deals were found on ModularGrid:\n\n"
                    
                    for i, deal in enumerate(deals, 1):
                        module_name = deal.get('module_name', '')
                        manufacturer = deal.get('manufacturer', '')
                        price = deal.get('current_pr
(Content truncated due to size limit. Use line ranges to read in chunks)