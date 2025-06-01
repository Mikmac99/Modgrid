"""
ModularGrid Price Monitor - Scraper Client
Client for interacting with ModularGrid website
"""
import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime

class ModularGridClient:
    """Client for scraping data from ModularGrid"""
    
    BASE_URL = "https://modulargrid.net"
    LOGIN_URL = f"{BASE_URL}/e/login"
    OFFERS_URL = f"{BASE_URL}/e/offers"
    
    def __init__(self, username, password):
        """Initialize with ModularGrid credentials"""
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged_in = False
        self.logger = logging.getLogger(__name__)
    
    def login(self):
        """Log in to ModularGrid"""
        if self.logged_in:
            return True
        
        try:
            # Get CSRF token
            response = self.session.get(self.LOGIN_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')
            
            # Submit login form
            login_data = {
                'csrf_token': csrf_token,
                'username': self.username,
                'password': self.password,
                'submit': 'Login'
            }
            
            response = self.session.post(self.LOGIN_URL, data=login_data)
            
            # Check if login was successful
            if 'Invalid username or password' in response.text:
                self.logger.error("Login failed: Invalid username or password")
                return False
            
            self.logged_in = True
            self.logger.info("Successfully logged in to ModularGrid")
            return True
            
        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            return False
    
    def get_module_listings(self, module_id):
        """Get current marketplace listings for a specific module"""
        if not self.logged_in and not self.login():
            return []
        
        try:
            # Search for the module in the marketplace
            search_url = f"{self.OFFERS_URL}?search={module_id}"
            response = self.session.get(search_url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all listings
            listings = []
            listing_elements = soup.select('.offer-item')
            
            for element in listing_elements:
                # Check if this listing is for the requested module
                module_link = element.select_one('.module-name a')
                if not module_link or str(module_id) not in module_link.get('href', ''):
                    continue
                
                # Extract listing data
                price_element = element.select_one('.price')
                price = float(price_element.text.strip().replace('$', '').replace(',', '')) if price_element else None
                
                condition_element = element.select_one('.condition')
                condition = condition_element.text.strip() if condition_element else 'Unknown'
                
                seller_element = element.select_one('.seller')
                seller = seller_element.text.strip() if seller_element else None
                
                location_element = element.select_one('.location')
                location = location_element.text.strip() if location_element else None
                
                date_element = element.select_one('.date')
                date_text = date_element.text.strip() if date_element else None
                date_listed = self._parse_date(date_text) if date_text else None
                
                # Get listing ID and URL
                listing_link = element.select_one('a.offer-link')
                url = f"{self.BASE_URL}{listing_link.get('href')}" if listing_link else None
                mg_listing_id = int(listing_link.get('href').split('/')[-1]) if listing_link else None
                
                listings.append({
                    'mg_listing_id': mg_listing_id,
                    'price': price,
                    'condition': condition,
                    'seller': seller,
                    'location': location,
                    'date_listed': date_listed,
                    'url': url
                })
            
            # Get average prices
            avg_prices = self._extract_average_prices(soup)
            
            # Combine listings with average prices
            result = {
                'listings': listings,
                'avg_price_new': avg_prices.get('new'),
                'avg_price_used': avg_prices.get('used')
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting module listings: {str(e)}")
            return []
    
    def get_module_details(self, module_id):
        """Get detailed information about a module"""
        if not self.logged_in and not self.login():
            return {}
        
        try:
            # Get module page
            module_url = f"{self.BASE_URL}/e/modules/view/{module_id}"
            response = self.session.get(module_url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract module data
            name_element = soup.select_one('h1.module-name')
            name = name_element.text.strip() if name_element else None
            
            manufacturer_element = soup.select_one('.manufacturer a')
            manufacturer = manufacturer_element.text.strip() if manufacturer_element else None
            
            # Extract technical specs
            specs = {}
            spec_elements = soup.select('.specs .spec')
            for element in spec_elements:
                label = element.select_one('.label')
                value = element.select_one('.value')
                if label and value:
                    key = label.text.strip().lower().replace(' ', '_')
                    specs[key] = value.text.strip()
            
            # Extract HP, depth, power
            hp = int(specs.get('width', '0').replace('HP', '').strip()) if 'width' in specs else None
            depth = float(specs.get('depth', '0').replace('mm', '').strip()) if 'depth' in specs else None
            power = specs.get('power_consumption', None)
            
            # Get price data
            price_elements = soup.select('.price-data')
            avg_price_new = None
            avg_price_used = None
            
            for element in price_elements:
                label = element.select_one('.label')
                value = element.select_one('.value')
                if label and value and 'Average price' in label.text:
                    price_text = value.text.strip().replace('$', '').replace(',', '')
                    if 'new' in label.text.lower():
                        avg_price_new = float(price_text) if price_text.replace('.', '').isdigit() else None
                    elif 'used' in label.text.lower():
                        avg_price_used = float(price_text) if price_text.replace('.', '').isdigit() else None
            
            return {
                'name': name,
                'manufacturer': manufacturer,
                'hp': hp,
                'depth': depth,
                'power': power,
                'avg_price_new': avg_price_new,
                'avg_price_used': avg_price_used
            }
            
        except Exception as e:
            self.logger.error(f"Error getting module details: {str(e)}")
            return {}
    
    def _extract_average_prices(self, soup):
        """Extract average prices from the page"""
        avg_prices = {}
        
        price_elements = soup.select('.price-data')
        for element in price_elements:
            label = element.select_one('.label')
            value = element.select_one('.value')
            if label and value and 'Average price' in label.text:
                price_text = value.text.strip().replace('$', '').replace(',', '')
                if 'new' in label.text.lower():
                    avg_prices['new'] = float(price_text) if price_text.replace('.', '').isdigit() else None
                elif 'used' in label.text.lower():
                    avg_prices['used'] = float(price_text) if price_text.replace('.', '').isdigit() else None
        
        return avg_prices
    
    def _parse_date(self, date_text):
        """Parse date text into datetime object"""
        try:
            # Handle relative dates
            if 'today' in date_text.lower():
                return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            elif 'yesterday' in date_text.lower():
                from datetime import timedelta
                return (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Handle absolute dates
            formats = ['%b %d, %Y', '%B %d, %Y', '%m/%d/%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_text, fmt)
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None
