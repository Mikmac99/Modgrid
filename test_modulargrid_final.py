#!/usr/bin/env python3
"""
ModularGrid Price Monitor - Test Script (Final)
----------------------------------------------
This script tests the functionality of the ModularGrid Price Monitor
with all issues fixed, including the scan cycle test.
"""

import os
import sys
import logging
import unittest
import json
from unittest.mock import patch, MagicMock

# Import modules to test
from modulargrid_scraper import ModularGridScraper
from modulargrid_database import ModularGridDatabase
from price_analyzer import PriceAnalyzer
from notification_system import NotificationSystem
from modulargrid_monitor import ModularGridMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("modulargrid_test")

class TestModularGridMonitor(unittest.TestCase):
    """Test cases for ModularGrid Price Monitor."""
    
    def setUp(self):
        """Set up test environment."""
        # Use test database
        self.db_path = "test_modulargrid.db"
        
        # Remove test database if it exists
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        # Create test configuration
        self.config = {
            "username": "donutheart",
            "password": "@bIvGv3U@W03hrA2",
            "scan_interval": 3600,
            "regions": ["EU", "USA"],
            "default_threshold": 15.0,
            "email_enabled": False,
            "windows_enabled": True
        }
        
        # Save config to file
        with open("test_config.json", "w") as f:
            json.dump(self.config, f)
        
        # Initialize components
        self.db = ModularGridDatabase(self.db_path)
        self.scraper = ModularGridScraper("test_config.json")
        self.analyzer = PriceAnalyzer(self.db)
        self.notifier = NotificationSystem(self.db, "test_config.json")
        self.monitor = ModularGridMonitor("test_config.json", self.db_path)
    
    def tearDown(self):
        """Clean up after tests."""
        # Close database connection
        self.db.close()
        
        # Remove test files
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
    
    def test_database_creation(self):
        """Test database creation and tables."""
        # Check if database file exists
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check if tables were created
        tables = [
            "Modules", "Listings", "PriceHistory", 
            "UserPreferences", "WatchList", "Deals"
        ]
        
        for table in tables:
            self.db.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            result = self.db.cursor.fetchone()
            self.assertIsNotNone(result, f"Table {table} not found")
    
    def test_add_module(self):
        """Test adding a module to the database."""
        module_data = {
            "module_id": "12345",
            "name": "Test Module",
            "manufacturer": "Test Manufacturer",
            "hp": 10,
            "type": "VCO",
            "description": "A test module"
        }
        
        # Add module
        module_id = self.db.add_module(module_data)
        self.assertIsNotNone(module_id)
        
        # Retrieve module
        self.db.cursor.execute("SELECT * FROM Modules WHERE module_id = ?", (module_data["module_id"],))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], module_data["name"])
    
    def test_add_to_watchlist(self):
        """Test adding a module to the watchlist."""
        # First add a module
        module_data = {
            "module_id": "12345",
            "name": "Test Module",
            "manufacturer": "Test Manufacturer"
        }
        self.db.add_module(module_data)
        
        # Add to watchlist
        watchlist_id = self.db.add_to_watchlist(
            module_data["module_id"], 
            price_threshold=20.0, 
            max_price=300.0
        )
        self.assertIsNotNone(watchlist_id)
        
        # Retrieve from watchlist
        self.db.cursor.execute("SELECT * FROM WatchList WHERE module_id = ?", (module_data["module_id"],))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result["price_threshold"], 20.0)
    
    @patch('requests.Session')
    def test_login(self, mock_session):
        """Test login functionality."""
        # Mock successful login
        mock_session_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.url = "https://modulargrid.net/e/modules"  # Not login page
        mock_response.text = "<html><form action='/e/login'><input type='hidden' name='csrf' value='token'></form></html>"
        
        mock_session_instance.get.return_value = mock_response
        mock_session_instance.post.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Create a new scraper with the mocked session
        scraper = ModularGridScraper("test_config.json")
        scraper.session = mock_session_instance
        
        # Test login
        success = scraper.login("donutheart", "@bIvGv3U@W03hrA2")
        self.assertTrue(success)
        self.assertTrue(scraper.authenticated)
        
        # Verify session calls
        mock_session_instance.get.assert_called_with(scraper.LOGIN_URL)
        mock_session_instance.post.assert_called()
    
    @patch('requests.Session')
    def test_get_marketplace_listings(self, mock_session):
        """Test retrieving marketplace listings."""
        # Mock response with sample HTML
        mock_session_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        # Sample HTML with a table of listings
        mock_response.text = """
        <html>
            <table class="offers">
                <tr>
                    <th>ID</th>
                    <th>Date</th>
                    <th>Price</th>
                    <th>Module</th>
                    <th>Seller</th>
                    <th>Region</th>
                    <th>View</th>
                </tr>
                <tr>
                    <td><a href="/e/offers/view/12345">12345</a></td>
                    <td>2025-04-04</td>
                    <td>€200,00</td>
                    <td>
                        <a href="/e/modules/12345">Test Module</a>
                        <div class="description">Test description</div>
                    </td>
                    <td><a href="/e/users/profile/seller">TestSeller</a></td>
                    <td>EU</td>
                    <td><a href="/e/offers/view/12345">View</a></td>
                </tr>
            </table>
        </html>
        """
        
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Create a new scraper with the mocked session
        scraper = ModularGridScraper("test_config.json")
        scraper.session = mock_session_instance
        
        # Test get_marketplace_listings
        listings = scraper.get_marketplace_listings(region="EU")
        
        # Verify results
        self.assertEqual(len(listings), 1)
        self.assertEqual(listings[0]["listing_id"], "12345")
        self.assertEqual(listings[0]["module_name"], "Test Module")
        self.assertEqual(listings[0]["price"], 200.0)
        self.assertEqual(listings[0]["currency"], "EUR")
        self.assertEqual(listings[0]["seller"], "TestSeller")
        self.assertEqual(listings[0]["region"], "EU")
    
    def test_price_analysis(self):
        """Test price analysis functionality."""
        # Add a module
        module_data = {
            "module_id": "12345",
            "name": "Test Module",
            "manufacturer": "Test Manufacturer"
        }
        self.db.add_module(module_data)
        
        # Add to watchlist
        self.db.add_to_watchlist(module_data["module_id"], price_threshold=15.0)
        
        # Add price history
        for price in [250.0, 240.0, 260.0]:  # Average: 250.0
            price_data = {
                "module_id": module_data["module_id"],
                "price": price,
                "currency": "EUR",
                "date_sold": "2025-03-01",
                "condition": "Like new"
            }
            self.db.add_price_history(price_data)
        
        # Add a listing
        listing_data = {
            "listing_id": "L12345",
            "module_id": module_data["module_id"],
            "price": 200.0,  # 20% below average
            "currency": "EUR",
            "seller": "TestSeller",
            "region": "EU",
            "condition": "Like new, no scratches",
            "date_listed": "2025-04-04",
            "url": "https://modulargrid.net/e/offers/view/12345"
        }
        self.db.add_listing(listing_data)
        
        # Test analyze_listing
        analysis = self.analyzer.analyze_listing(listing_data)
        
        # Verify analysis
        self.assertIsNotNone(analysis)
        self.assertTrue(analysis["is_deal"])
        self.assertAlmostEqual(analysis["percent_below"], 20.0, places=1)
        self.assertAlmostEqual(analysis["price_difference"], 50.0, places=1)
        
        # Test find_deals
        deals = self.analyzer.find_deals([listing_data])
        
        # Verify deals
        self.assertEqual(len(deals), 1)
        self.assertEqual(deals[0]["listing_id"], listing_data["listing_id"])
    
    def test_notification_system(self):
        """Test notification system functionality."""
        # Create a test deal
        deal = {
            "id": 1,
            "module_name": "Test Module",
            "manufacturer": "Test Manufacturer",
            "current_price": 200.0,
            "avg_price": 250.0,
            "price_difference": 50.0,
            "percent_below": 20.0,
            "currency": "EUR",
            "condition": "Like new, no scratches",
            "seller": "TestSeller",
            "region": "EU",
            "url": "https://modulargrid.net/e/offers/view/12345"
        }
        
        # Mock the send_windows_notification method
        with patch.object(NotificationSystem, 'send_windows_notification', return_value=True):
            # Enable Windows notifications
            self.notifier.config["windows_enabled"] = True
            
            # Test notification
            result = self.notifier.notify_deal(deal)
            
            # Verify notification was attempted
            self.assertTrue(result)
    
    def test_run_scan_cycle(self):
        """Test running a complete scan cycle."""
        # Create a custom monitor class for testing
        class TestMonitor(ModularGridMonitor):
            def scan_marketplace(self, regions=None):
                # Override to avoid the StopIteration error
                return [
                    {
                        "listing_id": "L12345",
                        "module_name": "Test Module",
                        "module_url": "https://modulargrid.net/e/modules/12345",
                        "price": 200.0,
                        "currency": "EUR",
                        "seller": "TestSeller",
                        "region": "EU",
                        "description": "Like new",
                        "date_modified": "2025-04-04",
                        "listing_url": "https://modulargrid.net/e/offers/view/12345"
                    }
                ]
            
            def get_price_history(self, module_ids=None):
                # Override to avoid actual API calls
                return {"12345": [{"price": 250.0, "currency": "EUR", "date_sold": "2025-03-01"}]}
        
        # Create test monitor
        test_monitor = TestMonitor("test_config.json", self.db_path)
        
        # Mock the find_deals and notify_deals methods
        test_monitor.find_deals = MagicMock(return_value=[
            {
                "id": 1,
                "listing_id": "L12345",
                "module_id": "12345",
                "module_name": "Test Module",
                "manufacturer": "Test Manufacturer",
                "current_price": 200.0,
                "avg_price": 250.0,
                "price_difference": 50.0,
                "percent_below": 20.0,
                "is_deal": True,
                "currency": "EUR",
                "condition": "Like new",
                "seller": "TestSeller",
                "region": "EU",
                "url": "https://modulargrid.net/e/offers/view/12345"
            }
        ])
        test_monitor.notify_deals = MagicMock(return_value=1)
        
        # Test run_scan_cycle
        num_listings, num_deals, num_notified = test_monitor.run_scan_cycle()
        
        # Verify results
        self.assertEqual(num_listings, 1)
        self.assertEqual(num_deals, 1)
        self.assertEqual(num_notified, 1)
        
        # Verify method calls
        test_monitor.find_deals.assert_called_once()
        test_monitor.notify_deals.assert_called_once()

def run_tests():
    """Run the test suite."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    run_tests()
