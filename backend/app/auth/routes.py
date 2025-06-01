"""
ModularGrid Price Monitor - Auth Routes
Authentication routes for user login, registration, etc.
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import auth_bp
from app.models.models import User
from app import db
from app.utils.crypto import encrypt_data, decrypt_data

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    # Create new user
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )
    
    # Add to database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user and return JWT token"""
    data = request.get_json()
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user_id': user.id,
        'username': user.username
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile information"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Don't return sensitive information
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'has_mg_credentials': bool(user.mg_username_encrypted),
        'price_threshold': user.price_threshold,
        'notify_email': user.notify_email
    }), 200

@auth_bp.route('/modulargrid-credentials', methods=['POST'])
@jwt_required()
def update_mg_credentials():
    """Update ModularGrid credentials"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Encrypt ModularGrid credentials
    user.mg_username_encrypted = encrypt_data(data['mg_username'])
    user.mg_password_encrypted = encrypt_data(data['mg_password'])
    
    db.session.commit()
    
    return jsonify({'message': 'ModularGrid credentials updated successfully'}), 200

@auth_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update user settings"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Update settings
    if 'price_threshold' in data:
        user.price_threshold = data['price_threshold']
    if 'notify_email' in data:
        user.notify_email = data['notify_email']
    
    db.session.commit()
    
    return jsonify({'message': 'Settings updated successfully'}), 200
