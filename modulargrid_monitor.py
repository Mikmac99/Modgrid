#!/usr/bin/env python3
"""
ModularGrid Price Monitor - Main Application
-------------------------------------------
This is the main application module for the ModularGrid Price Monitor.
It integrates the scraper, database, price analyzer, and notification system
to provide a complete solution for monitoring ModularGrid marketplace prices.
"""

import os
import sys
import time
import logging
import argparse
import json
import sqlite3
from datetime import datetime, timedelta

# Import custom modules
from modulargrid_scraper import ModularGridScraper
from modulargrid_database import ModularGridDatabase
from price_analyzer import PriceAnalyzer
from notification_system import NotificationSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("modulargrid_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("modulargrid_monitor")

class ModularGridMonitor:
    """Main application class for ModularGrid Price Monitor."""
    
    def __init__(self, config_file=None, db_path=None):
        """
        Initialize the ModularGrid Price Monitor.
        
        Args:
            config_file (str, optional): Path to configuration file
            db_path (str, optional): Path to database file
        """
        self.config = {}
        self.db_path = db_path or "modulargrid_monitor.db"
        
        # Load configuration
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        
        # Initialize components
        self.db = ModularGridDatabase(self.db_path)
        self.scraper = ModularGridScraper(config_file)
        self.analyzer = PriceAnalyzer(self.db)
        self.notifier = NotificationSystem(self.db, config_file)
        
        # Load configuration from database if not provided
        if not config_file:
            self._load_config_from_db()
        
        logger.info("ModularGrid Price Monitor initialized")
    
    def _load_config_from_db(self):
        """Load configuration from database preferences."""
        try:
            # Authentication settings
            self.config['username'] = self.db.get_preference('username', '')
            self.config['password'] = self.db.get_preference('password', '')
            
            # Scan settings
            self.config['scan_interval'] = int(self.db.get_preference('scan_interval', '3600'))
            self.config['regions'] = self.db.get_preference('regions', 'All').split(',')
            
            # Deal threshold
            self.config['default_threshold'] = float(self.db.get_preference('default_threshold', '15.0'))
            
            logger.info("Loaded configuration from database")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def save_config_to_db(self):
        """Save configuration to database preferences."""
        try:
            # Authentication settings
            self.db.set_preference('username', self.config.get('username', ''))
            self.db.set_preference('password', self.config.get('password', ''))
            
            # Scan settings
            self.db.set_preference('scan_interval', str(self.config.get('scan_interval', 3600)))
            self.db.set_preference('regions', ','.join(self.config.get('regions', ['All'])))
            
            # Deal threshold
            self.db.set_preference('default_threshold', str(self.config.get('default_threshold', 15.0)))
            
            logger.info("Saved configuration to database")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def authenticate(self, username=None, password=None):
        """
        Authenticate with ModularGrid.
        
        Args:
            username (str, optional): ModularGrid username
            password (str, optional): ModularGrid password
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        # Use provided credentials or load from config
        username = username or self.config.get('username', '')
        password = password or self.config.get('password', '')
        
        if not username or not password:
            logger.error("No credentials provided")
            return False
        
        # Attempt to log in
        success = self.scraper.login(username, password)
        
        if success:
            # Save credentials to config
            self.config['username'] = username
            self.config['password'] = password
            self.save_config_to_db()
        
        return success
    
    def scan_marketplace(self, regions=None):
        """
        Scan the ModularGrid marketplace for listings.
        
        Args:
            regions (list, optional): List of regions to scan
            
        Returns:
            list: List of listings found
        """
        # Use provided regions or load from config
        regions = regions or self.config.get('regions', ['All'])
        
        all_listings = []
        active_listing_ids = []
        
        # Handle 'All' region
        if 'All' in regions:
            regions = ['EU', 'USA', 'Canada', 'Australia', 'Asia', 'Africa', 'South America']
        
        # Scan each region
        for region in regions:
            logger.info(f"Scanning marketplace for region: {region}")
            
            # Get listings for current page
            page = 1
            while True:
                listings = self.scraper.get_marketplace_listings(region, page)
                
                if not listings:
                    break
                
                logger.info(f"Found {len(listings)} listings on page {page} for region {region}")
                
                # Process each listing
                for listing in listings:
                    # Extract module ID from module URL
                    module_url = listing.get('module_url', '')
                    module_id = module_url.split('/')[-1] if module_url else None
                    
                    if not module_id:
                        continue
                    
                    # Add module to database
                    module_data = {
                        'module_id': module_id,
                        'name': listing.get('module_name', ''),
                        'manufacturer': '',  # Will be populated later
                        'hp': 0,  # Will be populated later
                        'type': '',  # Will be populated later
                        'description': listing.get('description', '')
                    }
                    self.db.add_module(module_data)
                    
                    # Add listing to database
                    listing_data = {
                        'listing_id': listing.get('listing_id', ''),
                        'module_id': module_id,
                        'price': listing.get('price', 0.0),
                        'currency': listing.get('currency', 'EUR'),
                        'seller': listing.get('seller', ''),
                        'region': listing.get('region', ''),
                        'condition': listing.get('description', ''),
                        'date_listed': listing.get('date_modified', ''),
                        'url': listing.get('listing_url', '')
                    }
                    self.db.add_listing(listing_data)
                    
                    # Track active listing IDs
                    active_listing_ids.append(listing.get('listing_id', ''))
                    
                    # Add to results
                    all_listings.append(listing)
                
                # Move to next page
                page += 1
                
                # Avoid overloading the server
                time.sleep(1)
        
        # Mark inactive listings
        self.db.mark_inactive_listings(active_listing_ids)
        
        logger.info(f"Scan complete. Found {len(all_listings)} total listings.")
        return all_listings
    
    def get_price_history(self, module_ids=None):
        """
        Get price history for modules.
        
        Args:
            module_ids (list, optional): List of module IDs to get history for
            
        Returns:
            dict: Dictionary mapping module IDs to price history
        """
        if not self.scraper.authenticated:
            logger.warning("Not authenticated. Cannot get price history.")
            return {}
        
        # If no module IDs provided, get all modules in watchlist
        if not module_ids:
            watchlist = self.db.get_watchlist()
            module_ids = [item.get('module_id') for item in watchlist]
        
        price_history = {}
        
        for module_id in module_ids:
            logger.info(f"Getting price history for module: {module_id}")
            
            # Get module details
            module = self.db.get_module_by_id(module_id)
            if not module:
                logger.warning(f"Module not found: {module_id}")
                continue
            
            # Get a listing for this module to access its page
            self.db.cursor.execute(
                "SELECT url FROM Listings WHERE module_id = ? AND active = 1 LIMIT 1",
                (module_id,)
            )
            result = self.db.cursor.fetchone()
            
            if not result or not result['url']:
                logger.warning(f"No active listings found for module: {module_id}")
                continue
            
            # Get listing details including price history
            listing_url = result['url']
            details = self.scraper.get_listing_details(listing_url)
            
            if not details:
                logger.warning(f"Failed to get details for listing: {listing_url}")
                continue
            
            # Extract price history
            history = details.get('price_history', [])
            
            if not history:
                logger.info(f"No price history found for module: {module_id}")
                continue
            
            # Store price history in database
            for entry in history:
                price_data = {
                    'module_id': module_id,
                    'price': entry.get('price', 0.0),
                    'currency': entry.get('currency', 'EUR'),
                    'date_sold': entry.get('date_sold', ''),
                    'condition': entry.get('condition', '')
                }
                self.db.add_price_history(price_data)
            
            price_history[module_id] = history
            
            # Avoid overloading the server
            time.sleep(1)
        
        return price_history
    
    def find_deals(self):
        """
        Find good deals based on price comparison.
        
        Returns:
            list: List of good deals
        """
        logger.info("Finding deals...")
        
        # Get default threshold from config
        default_threshold = self.config.get('default_threshold', 15.0)
        
        # Use the analyzer to find deals
        deals = self.analyzer.find_deals()
        
        logger.info(f"Found {len(deals)} good deals")
        return deals
    
    def notify_deals(self, deals):
        """
        Send notifications for good deals.
        
        Args:
            deals (list): List of deals to notify
            
        Returns:
            int: Number of deals notified
        """
        if not deals:
            logger.info("No deals to notify")
            return 0
        
        logger.info(f"Sending notifications for {len(deals)} deals")
        return self.notifier.notify_deals(deals)
    
    def add_to_watchlist(self, module_id, threshold=None, max_price=None, currency='EUR'):
        """
        Add a module to the watchlist.
        
        Args:
            module_id (str): Module ID to watch
            threshold (float, optional): Price threshold percentage
            max_price (float, optional): Maximum price to consider
            currency (str): Currency code
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Use default threshold if not provided
        if threshold is None:
            threshold = self.config.get('default_threshold', 15.0)
        
        return self.db.add_to_watchlist(module_id, threshold, max_price, currency)
    
    def remove_from_watchlist(self, module_id):
        """
        Remove a module from the watchlist.
        
        Args:
            module_id (str): Module ID to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.db.remove_from_watchlist(module_id)
    
    def search_modules(self, query):
        """
        Search for modules by name.
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching modules
        """
        return self.scraper.search_modules(query)
    
    def run_scan_cycle(self):
        """
        Run a complete scan cycle: scan marketplace, get price history, find deals, notify.
        
        Returns:
            tuple: (num_listings, num_deals, num_notified)
        """
        logger.info("Starting scan cycle")
        
        # Ensure authenticated
        if not self.scraper.authenticated:
            username = self.config.get('username', '')
            password = self.config.get('password', '')
            
            if not username or not password:
                logger.error("No credentials available. Cannot run scan cycle.")
                return 0, 0, 0
            
            success = self.authenticate(username, password)
            if not success:
                logger.error("Authentication failed. Cannot run scan cycle.")
                return 0, 0, 0
        
        # Scan marketplace
        listings = self.scan_marketplace()
        
        # Get price history for watchlist modules
        self.get_price_history()
        
        # Find deals
        deals = self.find_deals()
        
        # Notify deals
        num_notified = self.notify_deals(deals)
        
        logger.info(f"Scan cycle complete: {len(listings)} listings, {len(deals)} deals, {num_notified} notifications")
        return len(listings), len(deals), num_notified
    
    def run_monitor(self, interval=None):
        """
        Run the monitor continuously.
        
        Args:
            interval (int, optional): Scan interval in seconds
            
        Returns:
            None
        """
        # Use provided interval or load from config
        interval = interval or self.config.get('scan_interval', 3600)
        
        logger.info(f"Starting continuous monitoring with interval {interval} seconds")
        
        try:
            while True:
                self.run_scan_cycle()
                
                logger.info(f"Sleeping for {interval} seconds")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        finally:
            self.db.close()
    
    def close(self):
        """Close database connection and clean up resources."""
        self.db.close()
        logger.info("ModularGrid Price Monitor closed")

def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(description="ModularGrid Price Monitor")
    parser.add_argument("--config", help="Path to con
(Content truncated due to size limit. Use line ranges to read in chunks)