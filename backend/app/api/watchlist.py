"""
ModularGrid Price Monitor - API Routes for Watchlist
API endpoints for user watchlist management
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models.models import WatchlistItem, Module
from app import db

@api_bp.route('/watchlist', methods=['GET'])
@jwt_required()
def get_watchlist():
    """Get user's watchlist items"""
    user_id = get_jwt_identity()
    
    # Get all watchlist items for the user
    watchlist_items = WatchlistItem.query.filter_by(user_id=user_id).all()
    
    result = [{
        'id': item.id,
        'module': {
            'id': item.module.id,
            'name': item.module.name,
            'manufacturer': item.module.manufacturer,
            'hp': item.module.hp,
            'avg_price_new': item.module.avg_price_new,
            'avg_price_used': item.module.avg_price_used
        },
        'max_price': item.max_price,
        'custom_threshold': item.custom_threshold,
        'date_added': item.date_added.isoformat()
    } for item in watchlist_items]
    
    return jsonify(result), 200

@api_bp.route('/watchlist', methods=['POST'])
@jwt_required()
def add_to_watchlist():
    """Add a module to user's watchlist"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if module exists
    module = Module.query.get(data['module_id'])
    if not module:
        return jsonify({'message': 'Module not found'}), 404
    
    # Check if already in watchlist
    existing = WatchlistItem.query.filter_by(
        user_id=user_id,
        module_id=data['module_id']
    ).first()
    
    if existing:
        return jsonify({'message': 'Module already in watchlist', 'id': existing.id}), 400
    
    # Create new watchlist item
    new_item = WatchlistItem(
        user_id=user_id,
        module_id=data['module_id'],
        max_price=data.get('max_price'),
        custom_threshold=data.get('custom_threshold')
    )
    
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Module added to watchlist',
        'id': new_item.id
    }), 201

@api_bp.route('/watchlist/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_watchlist_item(item_id):
    """Update watchlist item settings"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get watchlist item
    item = WatchlistItem.query.get_or_404(item_id)
    
    # Verify ownership
    if item.user_id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    # Update settings
    if 'max_price' in data:
        item.max_price = data['max_price']
    if 'custom_threshold' in data:
        item.custom_threshold = data['custom_threshold']
    
    db.session.commit()
    
    return jsonify({'message': 'Watchlist item updated successfully'}), 200

@api_bp.route('/watchlist/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_watchlist(item_id):
    """Remove a module from user's watchlist"""
    user_id = get_jwt_identity()
    
    # Get watchlist item
    item = WatchlistItem.query.get_or_404(item_id)
    
    # Verify ownership
    if item.user_id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    # Delete item
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Module removed from watchlist'}), 200
