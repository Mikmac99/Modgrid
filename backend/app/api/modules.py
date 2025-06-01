"""
ModularGrid Price Monitor - API Routes for Modules
API endpoints for module information
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models.models import Module, WatchlistItem
from app import db
from app.scraper.modulargrid_client import ModularGridClient

@api_bp.route('/modules', methods=['GET'])
@jwt_required()
def get_modules():
    """Get all modules or search by name/manufacturer"""
    search = request.args.get('search', '')
    
    query = Module.query
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Module.name.ilike(search_term)) | 
            (Module.manufacturer.ilike(search_term))
        )
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    modules = query.paginate(page=page, per_page=per_page)
    
    result = {
        'items': [{
            'id': module.id,
            'mg_id': module.mg_id,
            'name': module.name,
            'manufacturer': module.manufacturer,
            'hp': module.hp,
            'avg_price_new': module.avg_price_new,
            'avg_price_used': module.avg_price_used
        } for module in modules.items],
        'total': modules.total,
        'pages': modules.pages,
        'page': page
    }
    
    return jsonify(result), 200

@api_bp.route('/modules/<int:module_id>', methods=['GET'])
@jwt_required()
def get_module(module_id):
    """Get detailed information about a specific module"""
    module = Module.query.get_or_404(module_id)
    
    # Check if module is in user's watchlist
    user_id = get_jwt_identity()
    watchlist_item = WatchlistItem.query.filter_by(
        user_id=user_id, 
        module_id=module.id
    ).first()
    
    # Get price history (most recent first)
    price_history = [{
        'id': ph.id,
        'price': ph.price,
        'condition': ph.condition,
        'date': ph.date_recorded.isoformat()
    } for ph in module.price_history]
    
    # Get current listings
    listings = [{
        'id': listing.id,
        'price': listing.price,
        'condition': listing.condition,
        'seller': listing.seller,
        'location': listing.location,
        'date_listed': listing.date_listed.isoformat() if listing.date_listed else None,
        'url': listing.url,
        'is_deal': listing.is_deal,
        'deal_percentage': listing.deal_percentage
    } for listing in module.listings]
    
    result = {
        'id': module.id,
        'mg_id': module.mg_id,
        'name': module.name,
        'manufacturer': module.manufacturer,
        'hp': module.hp,
        'depth': module.depth,
        'power': module.power,
        'avg_price_new': module.avg_price_new,
        'avg_price_used': module.avg_price_used,
        'last_updated': module.last_updated.isoformat(),
        'in_watchlist': bool(watchlist_item),
        'watchlist_settings': {
            'max_price': watchlist_item.max_price if watchlist_item else None,
            'custom_threshold': watchlist_item.custom_threshold if watchlist_item else None
        } if watchlist_item else None,
        'price_history': price_history,
        'listings': listings
    }
    
    return jsonify(result), 200

@api_bp.route('/modules/refresh/<int:mg_id>', methods=['POST'])
@jwt_required()
def refresh_module(mg_id):
    """Refresh module data from ModularGrid"""
    user_id = get_jwt_identity()
    
    # Get user's ModularGrid credentials
    from app.models.models import User
    from app.utils.crypto import decrypt_data
    
    user = User.query.get(user_id)
    if not user.mg_username_encrypted or not user.mg_password_encrypted:
        return jsonify({'message': 'ModularGrid credentials not set'}), 400
    
    mg_username = decrypt_data(user.mg_username_encrypted)
    mg_password = decrypt_data(user.mg_password_encrypted)
    
    # Initialize ModularGrid client
    mg_client = ModularGridClient(mg_username, mg_password)
    
    # Refresh module data
    try:
        module_data = mg_client.get_module_details(mg_id)
        
        # Update or create module
        module = Module.query.filter_by(mg_id=mg_id).first()
        if not module:
            module = Module(mg_id=mg_id)
            db.session.add(module)
        
        # Update module data
        module.name = module_data['name']
        module.manufacturer = module_data['manufacturer']
        module.hp = module_data.get('hp')
        module.depth = module_data.get('depth')
        module.power = module_data.get('power')
        module.avg_price_new = module_data.get('avg_price_new')
        module.avg_price_used = module_data.get('avg_price_used')
        module.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Module data refreshed successfully',
            'module_id': module.id
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error refreshing module data: {str(e)}'}), 500
