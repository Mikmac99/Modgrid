"""
ModularGrid Price Monitor - Auth Blueprint
Authentication routes for the application
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Import and register routes
from app.auth import routes
