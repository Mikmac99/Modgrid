"""
ModularGrid Price Monitor - API Routes for Deals
API endpoints for deal information
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models.models import Listing, Module
from app import db
from datetime import datetime, timedelta

@api_bp.route('/deals', methods=['GET'])
@jwt_required()
def get_deals():
    """Get all deals or filter by various criteria"""
    # Get filter parameters
    manufacturer = request.args.get('manufacturer', '')
    min_discount = request.args.get('min_discount', 0, type=float)
    max_price = request.args.get('max_price', 0, type=float)
    days_listed = request.args.get('days_listed', 0, type=int)
    
    # Base query - only get listings marked as deals
    query = Listing.query.filter(Listing.is_deal == True)
    
    # Apply filters
    if manufacturer:
        query = query.join(Module).filter(Module.manufacturer.ilike(f"%{manufacturer}%"))
    
    if min_discount > 0:
        query = query.filter(Listing.deal_percentage >= min_discount)
    
    if max_price > 0:
        query = query.filter(Listing.price <= max_price)
    
    if days_listed > 0:
        date_threshold = datetime.utcnow() - timedelta(days=days_listed)
        query = query.filter(Listing.date_listed >= date_threshold)
    
    # Sort by best deals first (highest discount percentage)
    query = query.order_by(Listing.deal_percentage.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    deals = query.paginate(page=page, per_page=per_page)
    
    result = {
        'items': [{
            'id': deal.id,
            'module': {
                'id': deal.module.id,
                'name': deal.module.name,
                'manufacturer': deal.module.manufacturer,
                'hp': deal.module.hp
            },
            'price': deal.price,
            'condition': deal.condition,
            'seller': deal.seller,
            'location': deal.location,
            'date_listed': deal.date_listed.isoformat() if deal.date_listed else None,
            'url': deal.url,
            'deal_percentage': deal.deal_percentage,
            'date_found': deal.date_found.isoformat()
        } for deal in deals.items],
        'total': deals.total,
        'pages': deals.pages,
        'page': page
    }
    
    return jsonify(result), 200

@api_bp.route('/deals/<int:deal_id>', methods=['GET'])
@jwt_required()
def get_deal(deal_id):
    """Get detailed information about a specific deal"""
    deal = Listing.query.get_or_404(deal_id)
    
    if not deal.is_deal:
        return jsonify({'message': 'This listing is not marked as a deal'}), 404
    
    result = {
        'id': deal.id,
        'module': {
            'id': deal.module.id,
            'name': deal.module.name,
            'manufacturer': deal.module.manufacturer,
            'hp': deal.module.hp,
            'avg_price_new': deal.module.avg_price_new,
            'avg_price_used': deal.module.avg_price_used
        },
        'price': deal.price,
        'condition': deal.condition,
        'seller': deal.seller,
        'location': deal.location,
        'date_listed': deal.date_listed.isoformat() if deal.date_listed else None,
        'url': deal.url,
        'deal_percentage': deal.deal_percentage,
        'date_found': deal.date_found.isoformat(),
        'comparable_listings': [{
            'id': listing.id,
            'price': listing.price,
            'condition': listing.condition,
            'date_listed': listing.date_listed.isoformat() if listing.date_listed else None
        } for listing in Listing.query.filter(
            Listing.module_id == deal.module_id,
            Listing.id != deal.id
        ).limit(5)]
    }
    
    return jsonify(result), 200
