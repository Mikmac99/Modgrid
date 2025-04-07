#!/usr/bin/env python3
"""
ModularGrid Marketplace Scraper
-------------------------------
This module handles web scraping functionality for the ModularGrid Price Monitor.
It includes functions to authenticate with ModularGrid, scrape marketplace listings,
and extract price history data.
"""

import os
import time
import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("modulargrid_scraper")

class ModularGridScraper:
    """Class to handle scraping of ModularGrid marketplace data."""
    
    BASE_URL = "https://modulargrid.net"
    MARKETPLACE_URL = "https://modulargrid.net/e/offers"
    LOGIN_URL = "https://modulargrid.net/e/login"
    
    def __init__(self, config_file=None):
        """Initialize the scraper with optional configuration file."""
        self.session = requests.Session()
        self.authenticated = False
        self.config = {}
        
        # Load configuration if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        
        # Set up headers to mimic a browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    
    def _encrypt_credentials(self, username, password, key=None):
        """Encrypt credentials for secure storage."""
        if not key:
            key = Fernet.generate_key()
        
        cipher_suite = Fernet(key)
        encrypted_username = cipher_suite.encrypt(username.encode())
        encrypted_password = cipher_suite.encrypt(password.encode())
        
        return {
            'key': key.decode() if isinstance(key, bytes) else key,
            'username': encrypted_username.decode(),
            'password': encrypted_password.decode()
        }
    
    def _decrypt_credentials(self, encrypted_data):
        """Decrypt stored credentials."""
        cipher_suite = Fernet(encrypted_data['key'].encode())
        username = cipher_suite.decrypt(encrypted_data['username'].encode()).decode()
        password = cipher_suite.decrypt(encrypted_data['password'].encode()).decode()
        
        return username, password
    
    def save_credentials(self, username, password, file_path):
        """Securely save credentials to a file."""
        encrypted = self._encrypt_credentials(username, password)
        
        with open(file_path, 'w') as f:
            json.dump(encrypted, f)
        
        logger.info(f"Credentials saved to {file_path}")
    
    def load_credentials(self, file_path):
        """Load encrypted credentials from a file."""
        if not os.path.exists(file_path):
            logger.error(f"Credentials file not found: {file_path}")
            return None, None
        
        with open(file_path, 'r') as f:
            encrypted = json.load(f)
        
        return self._decrypt_credentials(encrypted)
    
    def login(self, username, password):
        """Log in to ModularGrid with the provided credentials."""
        logger.info("Attempting to log in to ModularGrid...")
        
        # First, get the login page to retrieve any CSRF tokens
        response = self.session.get(self.LOGIN_URL)
        if response.status_code != 200:
            logger.error(f"Failed to access login page: {response.status_code}")
            return False
        
        # Parse the login form
        soup = BeautifulSoup(response.text, 'html.parser')
        login_form = soup.find('form', {'action': '/e/login'})
        
        if not login_form:
            logger.error("Login form not found on page")
            return False
        
        # Extract any hidden fields (like CSRF tokens)
        form_data = {}
        for input_field in login_form.find_all('input', {'type': 'hidden'}):
            form_data[input_field.get('name')] = input_field.get('value', '')
        
        # Add username and password
        form_data['username'] = username
        form_data['password'] = password
        form_data['remember'] = '1'  # Keep me logged in
        
        # Submit the login form
        login_response = self.session.post(
            self.LOGIN_URL,
            data=form_data,
            headers={'Referer': self.LOGIN_URL}
        )
        
        # Check if login was successful
        if login_response.url != self.LOGIN_URL and "login" not in login_response.url:
            logger.info("Login successful")
            self.authenticated = True
            return True
        else:
            logger.error("Login failed")
            return False
    
    def get_marketplace_listings(self, region=None, page=1):
        """
        Scrape marketplace listings with optional region filtering.
        
        Args:
            region (str, optional): Filter by region (e.g., 'EU', 'USA')
            page (int, optional): Page number for pagination
            
        Returns:
            list: List of dictionaries containing listing data
        """
        logger.info(f"Fetching marketplace listings (page {page})")
        
        # Construct URL with parameters
        url = self.MARKETPLACE_URL
        params = {}
        
        if region:
            params['region'] = region
        
        if page > 1:
            params['page'] = page
        
        # Make the request
        response = self.session.get(url, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to fetch marketplace: {response.status_code}")
            return []
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = []
        
        # Find the table containing listings
        table = soup.find('table', {'class': 'offers'})
        if not table:
            logger.warning("No listings table found on page")
            return []
        
        # Process each row in the table (skip header row)
        for row in table.find_all('tr')[1:]:
            try:
                cells = row.find_all('td')
                if len(cells) < 6:
                    continue
                
                # Extract listing data
                listing_id = cells[0].find('a').get('href').split('/')[-1]
                date_modified = cells[1].text.strip()
                price_text = cells[2].text.strip()
                
                # Parse price and currency
                price, currency = self._parse_price(price_text)
                
                # Get module name and link
                module_link = cells[3].find('a')
                module_name = module_link.text.strip()
                module_url = urljoin(self.BASE_URL, module_link.get('href'))
                
                # Get module description
                module_desc = cells[3].find('div', {'class': 'description'})
                description = module_desc.text.strip() if module_desc else ""
                
                # Get seller and region
                seller = cells[4].find('a').text.strip()
                region = cells[5].text.strip()
                
                # Get listing URL
                view_link = cells[6].find('a')
                listing_url = urljoin(self.BASE_URL, view_link.get('href')) if view_link else None
                
                # Create listing object
                listing = {
                    'listing_id': listing_id,
                    'date_modified': date_modified,
                    'price': price,
                    'currency': currency,
                    'module_name': module_name,
                    'module_url': module_url,
                    'description': description,
                    'seller': seller,
                    'region': region,
                    'listing_url': listing_url,
                    'last_checked': datetime.now().isoformat()
                }
                
                listings.append(listing)
                
            except Exception as e:
                logger.error(f"Error parsing listing row: {e}")
                continue
        
        logger.info(f"Found {len(listings)} listings on page {page}")
        return listings
    
    def get_listing_details(self, listing_url):
        """
        Get detailed information about a specific listing.
        
        Args:
            listing_url (str): URL of the listing
            
        Returns:
            dict: Detailed listing information
        """
        logger.info(f"Fetching details for listing: {listing_url}")
        
        response = self.session.get(listing_url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch listing details: {response.status_code}")
            return {}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        details = {}
        
        # Extract listing details
        try:
            # Get module name
            module_name = soup.find('h1').text.strip()
            details['module_name'] = module_name
            
            # Get price
            price_elem = soup.find('tr', text=lambda t: t and 'Price' in t)
            if price_elem and price_elem.find_next('td'):
                price_text = price_elem.find_next('td').text.strip()
                price, currency = self._parse_price(price_text)
                details['price'] = price
                details['currency'] = currency
            
            # Get condition description
            description_div = soup.find('div', {'class': 'description'})
            if description_div:
                details['condition'] = description_div.text.strip()
            
            # Get seller info
            seller_elem = soup.find('tr', text=lambda t: t and 'Seller' in t)
            if seller_elem and seller_elem.find_next('td'):
                details['seller'] = seller_elem.find_next('td').text.strip()
            
            # Get region
            region_elem = soup.find('tr', text=lambda t: t and 'Region' in t)
            if region_elem and region_elem.find_next('td'):
                details['region'] = region_elem.find_next('td').text.strip()
            
            # Get price history (Unicorn account feature)
            price_history = self._extract_price_history(soup)
            if price_history:
                details['price_history'] = price_history
            
        except Exception as e:
            logger.error(f"Error parsing listing details: {e}")
        
        return details
    
    def _extract_price_history(self, soup):
        """
        Extract price history from a listing page (requires Unicorn account).
        
        Args:
            soup (BeautifulSoup): Parsed HTML of the listing page
            
        Returns:
            list: List of historical price data
        """
        price_history = []
        
        # Look for the price history section
        history_section = soup.find('h2', text=lambda t: t and 'Price History' in t)
        if not history_section:
            logger.debug("No price history section found (may require Unicorn account)")
            return price_history
        
        # Find the table containing price history
        history_table = history_section.find_next('table')
        if not history_table:
            return price_history
        
        # Process each row in the history table
        for row in history_table.find_all('tr')[1:]:  # Skip header row
            try:
                cells = row.find_all('td')
                if len(cells) < 3:
                    continue
                
                date_sold = cells[0].text.strip()
                price_text = cells[1].text.strip()
                price, currency = self._parse_price(price_text)
                condition = cells[2].text.strip() if len(cells) > 2 else ""
                
                price_history.append({
                    'date_sold': date_sold,
                    'price': price,
                    'currency': currency,
                    'condition': condition
                })
                
            except Exception as e:
                logger.error(f"Error parsing price history row: {e}")
                continue
        
        logger.info(f"Found {len(price_history)} historical price entries")
        return price_history
    
    def _parse_price(self, price_text):
        """
        Parse price and currency from a price string.
        
        Args:
            price_text (str): Price text (e.g., "€200,00" or "$150.00")
            
        Returns:
            tuple: (price as float, currency code)
        """
        # Default values
        price = 0.0
        currency = "EUR"  # Default to EUR
        
        try:
            # Identify currency symbol
            if price_text.startswith('€'):
                currency = "EUR"
                price_text = price_text.replace('€', '').strip()
            elif price_text.startswith('$'):
                currency = "USD"
                price_text = price_text.replace('$', '').strip()
            elif price_text.startswith('£'):
                currency = "GBP"
                price_text = price_text.replace('£', '').strip()
            elif price_text.startswith('¥'):
                currency = "JPY"
                price_text = price_text.replace('¥', '').strip()
            
            # Handle different number formats
            price_text = price_text.replace(',', '.')
            
            # Extract the first valid number
            import re
            number_match = re.search(r'\d+(?:\.\d+)?', price_text)
            if number_match:
                price = float(number_match.group())
            
        except Exception as e:
            logger.error(f"Error parsing price '{price_text}': {e}")
        
        return price, currency
    
    def search_modules(self, query):
        """
        Search for modules by name.
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching modules
        """
        logger.info(f"Searching for modules: {query}")
        
        search_url = f"{self.BASE_URL}/e/modules/browser"
        params = {'q': query}
        
        response = self.session.get(search_url, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to search modules: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        modules = []
        
        # Find module results
        module_table = soup.find('table', {'class': 'modules'})
        if not module_table:
            return modules
        
        # Process each row
        for row in module_table.find_all('tr')[1:]:  # Skip header row
            try:
                cells = row.find_all('td')
                if len(cells) < 3:
                    continue
                
                # Extract module data
                module_link = cells[1].find('a')
                if not module_link:
                    continue
                
                module_name = module_link.text.strip()
                module_url = urljoin(self.BASE_URL, module_link.get('href'))
                module_id = module_url.split('/')[-1]
                
                # Get manufacturer
                manufacturer = cells[0].text.stri
(Content truncated due to size limit. Use line ranges to read in chunks)