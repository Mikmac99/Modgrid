"""
ModularGrid Price Monitor - Models
Database models for the application
"""
from datetime import datetime
from app import db

class User(db.Model):
    """User model for authentication and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ModularGrid credentials (encrypted)
    mg_username_encrypted = db.Column(db.Text, nullable=True)
    mg_password_encrypted = db.Column(db.Text, nullable=True)
    
    # User preferences
    price_threshold = db.Column(db.Float, default=15.0)  # % below average to consider a deal
    notify_email = db.Column(db.Boolean, default=True)
    
    # Relationships
    watchlist_items = db.relationship('WatchlistItem', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Module(db.Model):
    """Eurorack module information"""
    id = db.Column(db.Integer, primary_key=True)
    mg_id = db.Column(db.Integer, unique=True, nullable=False)  # ModularGrid ID
    name = db.Column(db.String(200), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    hp = db.Column(db.Integer, nullable=True)  # Width in HP
    depth = db.Column(db.Float, nullable=True)  # Depth in mm
    power = db.Column(db.String(50), nullable=True)  # Power requirements
    avg_price_new = db.Column(db.Float, nullable=True)
    avg_price_used = db.Column(db.Float, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    price_history = db.relationship('PriceHistory', backref='module', lazy=True)
    listings = db.relationship('Listing', backref='module', lazy=True)
    watchlist_items = db.relationship('WatchlistItem', backref='module', lazy=True)
    
    def __repr__(self):
        return f"Module('{self.name}', '{self.manufacturer}')"

class PriceHistory(db.Model):
    """Historical price data for modules"""
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=False)  # New, Used, etc.
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"PriceHistory(Module ID: {self.module_id}, Price: {self.price})"

class Listing(db.Model):
    """Current marketplace listings"""
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    mg_listing_id = db.Column(db.Integer, unique=True, nullable=False)  # ModularGrid listing ID
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    seller = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    date_listed = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    is_deal = db.Column(db.Boolean, default=False)
    deal_percentage = db.Column(db.Float, nullable=True)  # % below average price
    date_found = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Listing(Module ID: {self.module_id}, Price: {self.price})"

class WatchlistItem(db.Model):
    """User's watchlist for specific modules"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    max_price = db.Column(db.Float, nullable=True)  # Maximum price user is willing to pay
    custom_threshold = db.Column(db.Float, nullable=True)  # Custom % threshold for this module
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"WatchlistItem(User ID: {self.user_id}, Module ID: {self.module_id})"

class Notification(db.Model):
    """Notifications for users about deals"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    read = db.Column(db.Boolean, default=False)
    emailed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    listing = db.relationship('Listing', backref='notifications')
    
    def __repr__(self):
        return f"Notification(User ID: {self.user_id}, Listing ID: {self.listing_id})"
