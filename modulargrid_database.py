#!/usr/bin/env python3
"""
ModularGrid Database Module
---------------------------
This module handles database operations for the ModularGrid Price Monitor.
It includes functions to create and manage the SQLite database, store and
retrieve module listings, price history, and user preferences.
"""

import os
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("modulargrid_database")

class ModularGridDatabase:
    """Class to handle database operations for ModularGrid Price Monitor."""
    
    def __init__(self, db_path="modulargrid_monitor.db"):
        """Initialize the database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Connect to database
        self._connect()
        
        # Create tables if they don't exist
        self._create_tables()
    
    def _connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        try:
            # Modules table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                manufacturer TEXT,
                hp INTEGER,
                type TEXT,
                description TEXT
            )
            ''')
            
            # Listings table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT UNIQUE NOT NULL,
                module_id TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL,
                seller TEXT,
                region TEXT,
                condition TEXT,
                date_listed TEXT,
                url TEXT,
                last_checked TIMESTAMP,
                active BOOLEAN DEFAULT 1,
                FOREIGN KEY (module_id) REFERENCES Modules(module_id)
            )
            ''')
            
            # PriceHistory table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PriceHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL,
                date_sold TEXT,
                condition TEXT,
                FOREIGN KEY (module_id) REFERENCES Modules(module_id)
            )
            ''')
            
            # UserPreferences table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserPreferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_name TEXT UNIQUE NOT NULL,
                setting_value TEXT
            )
            ''')
            
            # WatchList table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS WatchList (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id TEXT NOT NULL,
                price_threshold REAL,
                max_price REAL,
                currency TEXT,
                notify BOOLEAN DEFAULT 1,
                FOREIGN KEY (module_id) REFERENCES Modules(module_id)
            )
            ''')
            
            # Deals table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT NOT NULL,
                detected_date TIMESTAMP,
                avg_price REAL,
                price_difference REAL,
                percentage_below REAL,
                notified BOOLEAN DEFAULT 0,
                FOREIGN KEY (listing_id) REFERENCES Listings(listing_id)
            )
            ''')
            
            # Create indexes
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_modules_module_id ON Modules(module_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_listings_module_id ON Listings(module_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_listings_listing_id ON Listings(listing_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_pricehistory_module_id ON PriceHistory(module_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_watchlist_module_id ON WatchList(module_id)')
            
            self.conn.commit()
            logger.info("Database tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def add_module(self, module_data):
        """
        Add a module to the database.
        
        Args:
            module_data (dict): Module information
            
        Returns:
            int: ID of the inserted module
        """
        try:
            # Check if module already exists
            self.cursor.execute(
                "SELECT id FROM Modules WHERE module_id = ?",
                (module_data.get('module_id'),)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing module
                self.cursor.execute(
                    """
                    UPDATE Modules SET
                        name = ?,
                        manufacturer = ?,
                        hp = ?,
                        type = ?,
                        description = ?
                    WHERE module_id = ?
                    """,
                    (
                        module_data.get('name', ''),
                        module_data.get('manufacturer', ''),
                        module_data.get('hp', 0),
                        module_data.get('type', ''),
                        module_data.get('description', ''),
                        module_data.get('module_id')
                    )
                )
                self.conn.commit()
                logger.info(f"Updated module: {module_data.get('name')}")
                return existing['id']
            else:
                # Insert new module
                self.cursor.execute(
                    """
                    INSERT INTO Modules (
                        module_id, name, manufacturer, hp, type, description
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        module_data.get('module_id', ''),
                        module_data.get('name', ''),
                        module_data.get('manufacturer', ''),
                        module_data.get('hp', 0),
                        module_data.get('type', ''),
                        module_data.get('description', '')
                    )
                )
                self.conn.commit()
                logger.info(f"Added new module: {module_data.get('name')}")
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding module: {e}")
            self.conn.rollback()
            raise
    
    def add_listing(self, listing_data):
        """
        Add a marketplace listing to the database.
        
        Args:
            listing_data (dict): Listing information
            
        Returns:
            int: ID of the inserted listing
        """
        try:
            # Check if listing already exists
            self.cursor.execute(
                "SELECT id FROM Listings WHERE listing_id = ?",
                (listing_data.get('listing_id'),)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing listing
                self.cursor.execute(
                    """
                    UPDATE Listings SET
                        module_id = ?,
                        price = ?,
                        currency = ?,
                        seller = ?,
                        region = ?,
                        condition = ?,
                        date_listed = ?,
                        url = ?,
                        last_checked = ?,
                        active = 1
                    WHERE listing_id = ?
                    """,
                    (
                        listing_data.get('module_id', ''),
                        listing_data.get('price', 0.0),
                        listing_data.get('currency', 'EUR'),
                        listing_data.get('seller', ''),
                        listing_data.get('region', ''),
                        listing_data.get('condition', ''),
                        listing_data.get('date_listed', ''),
                        listing_data.get('url', ''),
                        datetime.now().isoformat(),
                        listing_data.get('listing_id')
                    )
                )
                self.conn.commit()
                logger.info(f"Updated listing: {listing_data.get('listing_id')}")
                return existing['id']
            else:
                # Insert new listing
                self.cursor.execute(
                    """
                    INSERT INTO Listings (
                        listing_id, module_id, price, currency, seller,
                        region, condition, date_listed, url, last_checked, active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (
                        listing_data.get('listing_id', ''),
                        listing_data.get('module_id', ''),
                        listing_data.get('price', 0.0),
                        listing_data.get('currency', 'EUR'),
                        listing_data.get('seller', ''),
                        listing_data.get('region', ''),
                        listing_data.get('condition', ''),
                        listing_data.get('date_listed', ''),
                        listing_data.get('url', ''),
                        datetime.now().isoformat()
                    )
                )
                self.conn.commit()
                logger.info(f"Added new listing: {listing_data.get('listing_id')}")
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding listing: {e}")
            self.conn.rollback()
            raise
    
    def add_price_history(self, price_data):
        """
        Add a historical price entry to the database.
        
        Args:
            price_data (dict): Price history information
            
        Returns:
            int: ID of the inserted price history entry
        """
        try:
            # Check if this exact price history entry already exists
            self.cursor.execute(
                """
                SELECT id FROM PriceHistory 
                WHERE module_id = ? AND price = ? AND currency = ? AND date_sold = ?
                """,
                (
                    price_data.get('module_id', ''),
                    price_data.get('price', 0.0),
                    price_data.get('currency', 'EUR'),
                    price_data.get('date_sold', '')
                )
            )
            existing = self.cursor.fetchone()
            
            if existing:
                logger.debug(f"Price history entry already exists: {price_data}")
                return existing['id']
            else:
                # Insert new price history entry
                self.cursor.execute(
                    """
                    INSERT INTO PriceHistory (
                        module_id, price, currency, date_sold, condition
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        price_data.get('module_id', ''),
                        price_data.get('price', 0.0),
                        price_data.get('currency', 'EUR'),
                        price_data.get('date_sold', ''),
                        price_data.get('condition', '')
                    )
                )
                self.conn.commit()
                logger.info(f"Added price history for module: {price_data.get('module_id')}")
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding price history: {e}")
            self.conn.rollback()
            raise
    
    def add_to_watchlist(self, module_id, price_threshold=15.0, max_price=None, currency='EUR'):
        """
        Add a module to the watchlist.
        
        Args:
            module_id (str): Module ID to watch
            price_threshold (float): Percentage below average to trigger alert
            max_price (float, optional): Maximum price to consider
            currency (str): Currency code for max_price
            
        Returns:
            int: ID of the watchlist entry
        """
        try:
            # Check if module is already in watchlist
            self.cursor.execute(
                "SELECT id FROM WatchList WHERE module_id = ?",
                (module_id,)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing watchlist entry
                self.cursor.execute(
                    """
                    UPDATE WatchList SET
                        price_threshold = ?,
                        max_price = ?,
                        currency = ?,
                        notify = 1
                    WHERE module_id = ?
                    """,
                    (price_threshold, max_price, currency, module_id)
                )
                self.conn.commit()
                logger.info(f"Updated watchlist entry for module: {module_id}")
                return existing['id']
            else:
                # Insert new watchlist entry
                self.cursor.execute(
                    """
                    INSERT INTO WatchList (
                        module_id, price_threshold, max_price, currency, notify
                    ) VALUES (?, ?, ?, ?, 1)
                    """,
                    (module_id, price_threshold, max_price, currency)
                )
                self.conn.commit()
                logger.info(f"Added module to watchlist: {module_id}")
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding to watchlist: {e}")
            self.conn.rollback()
            raise
    
    def remove_from_watchlist(self, module_id):
        """
        Remove a module from the watchlist.
        
        Args:
            module_id (str): Module ID to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.execute(
                "DELETE FROM WatchList WHERE module_id = ?",
                (module_id,)
            )
            self.conn.commit()
            logger.info(f"Removed module from watchlist: {module_id}")
            return True
        except sqlite3.Error as e:
      
(Content truncated due to size limit. Use line ranges to read in chunks)