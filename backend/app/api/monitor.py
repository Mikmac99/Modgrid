"""
ModularGrid Price Monitor - API Routes for Monitor
API endpoints for monitoring functionality
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models.models import User, Module, Listing, WatchlistItem, Notification
from app import db
from app.scraper.modulargrid_client import ModularGridClient
from app.scraper.price_analyzer import PriceAnalyzer
from app.utils.crypto import decrypt_data
from datetime import datetime

@api_bp.route('/monitor/status', methods=['GET'])
@jwt_required()
def get_monitor_status():
    """Get current monitoring status"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user has ModularGrid credentials
    has_credentials = bool(user.mg_username_encrypted and user.mg_password_encrypted)
    
    # Get monitoring statistics
    watchlist_count = WatchlistItem.query.filter_by(user_id=user_id).count()
    deals_found = Listing.query.filter(
        Listing.is_deal == True,
        Listing.module_id.in_(
            db.session.query(WatchlistItem.module_id).filter_by(user_id=user_id)
        )
    ).count()
    
    # Get last scan time (if any)
    # This would typically be stored in a separate table, but for simplicity
    # we'll just use the most recent notification or listing
    last_notification = Notification.query.filter_by(user_id=user_id).order_by(
        Notification.date_created.desc()
    ).first()
    
    last_scan_time = last_notification.date_created if last_notification else None
    
    result = {
        'has_credentials': has_credentials,
        'watchlist_count': watchlist_count,
        'deals_found': deals_found,
        'last_scan_time': last_scan_time.isoformat() if last_scan_time else None,
        'price_threshold': user.price_threshold,
        'notify_email': user.notify_email
    }
    
    return jsonify(result), 200

@api_bp.route('/monitor/scan', methods=['POST'])
@jwt_required()
def run_scan():
    """Run a manual scan for deals"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user has ModularGrid credentials
    if not user.mg_username_encrypted or not user.mg_password_encrypted:
        return jsonify({'message': 'ModularGrid credentials not set'}), 400
    
    # Get user's watchlist
    watchlist_items = WatchlistItem.query.filter_by(user_id=user_id).all()
    if not watchlist_items:
        return jsonify({'message': 'Watchlist is empty'}), 400
    
    # Decrypt ModularGrid credentials
    mg_username = decrypt_data(user.mg_username_encrypted)
    mg_password = decrypt_data(user.mg_password_encrypted)
    
    # Initialize ModularGrid client and price analyzer
    mg_client = ModularGridClient(mg_username, mg_password)
    price_analyzer = PriceAnalyzer()
    
    # Track results
    new_deals_found = 0
    modules_scanned = 0
    
    try:
        # Scan each module in the watchlist
        for item in watchlist_items:
            module = Module.query.get(item.module_id)
            if not module:
                continue
            
            # Get current listings for this module
            listings = mg_client.get_module_listings(module.mg_id)
            modules_scanned += 1
            
            # Analyze each listing for deals
            for listing_data in listings:
                # Check if listing already exists
                existing = Listing.query.filter_by(mg_listing_id=listing_data['mg_listing_id']).first()
                if existing:
                    continue
                
                # Determine if this is a deal
                threshold = item.custom_threshold or user.price_threshold
                is_deal, deal_percentage = price_analyzer.is_deal(
                    listing_data['price'],
                    listing_data['condition'],
                    module.avg_price_new,
                    module.avg_price_used,
                    threshold
                )
                
                # If it's a deal or we're tracking all listings
                if is_deal or item.max_price and listing_data['price'] <= item.max_price:
                    # Create new listing
                    new_listing = Listing(
                        module_id=module.id,
                        mg_listing_id=listing_data['mg_listing_id'],
                        price=listing_data['price'],
                        condition=listing_data['condition'],
                        seller=listing_data.get('seller'),
                        location=listing_data.get('location'),
                        date_listed=listing_data.get('date_listed'),
                        url=listing_data.get('url'),
                        is_deal=is_deal,
                        deal_percentage=deal_percentage
                    )
                    
                    db.session.add(new_listing)
                    db.session.flush()  # Get ID without committing
                    
                    # Create notification
                    notification = Notification(
                        user_id=user_id,
                        listing_id=new_listing.id,
                        read=False,
                        emailed=False
                    )
                    
                    db.session.add(notification)
                    new_deals_found += 1
            
            # Update module's price data
            module.avg_price_new = listings.get('avg_price_new', module.avg_price_new)
            module.avg_price_used = listings.get('avg_price_used', module.avg_price_used)
            module.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Scan completed successfully',
            'modules_scanned': modules_scanned,
            'new_deals_found': new_deals_found
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error during scan: {str(e)}'}), 500
