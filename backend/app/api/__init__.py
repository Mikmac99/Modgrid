"""
ModularGrid Price Monitor - API Blueprint
API routes for the application
"""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import and register routes
from app.api import modules, deals, watchlist, monitor, notifications

# Add more routes as needed
