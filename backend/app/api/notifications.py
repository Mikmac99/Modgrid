"""
ModularGrid Price Monitor - API Routes for Notifications
API endpoints for user notifications
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models.models import Notification, Listing
from app import db
from datetime import datetime

@api_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user's notifications"""
    user_id = get_jwt_identity()
    
    # Filter parameters
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    # Base query
    query = Notification.query.filter_by(user_id=user_id)
    
    # Apply filters
    if unread_only:
        query = query.filter_by(read=False)
    
    # Sort by newest first
    query = query.order_by(Notification.date_created.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    notifications = query.paginate(page=page, per_page=per_page)
    
    result = {
        'items': [{
            'id': notification.id,
            'listing': {
                'id': notification.listing.id,
                'module': {
                    'id': notification.listing.module.id,
                    'name': notification.listing.module.name,
                    'manufacturer': notification.listing.module.manufacturer
                },
                'price': notification.listing.price,
                'condition': notification.listing.condition,
                'deal_percentage': notification.listing.deal_percentage,
                'url': notification.listing.url
            },
            'read': notification.read,
            'emailed': notification.emailed,
            'date_created': notification.date_created.isoformat()
        } for notification in notifications.items],
        'total': notifications.total,
        'pages': notifications.pages,
        'page': page,
        'unread_count': Notification.query.filter_by(user_id=user_id, read=False).count()
    }
    
    return jsonify(result), 200

@api_bp.route('/notifications/mark-read', methods=['POST'])
@jwt_required()
def mark_notifications_read():
    """Mark notifications as read"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get notification IDs to mark as read
    notification_ids = data.get('notification_ids', [])
    
    if not notification_ids:
        # Mark all as read if no specific IDs provided
        notifications = Notification.query.filter_by(user_id=user_id, read=False).all()
        for notification in notifications:
            notification.read = True
        
        db.session.commit()
        return jsonify({'message': 'All notifications marked as read'}), 200
    
    # Mark specific notifications as read
    notifications = Notification.query.filter(
        Notification.id.in_(notification_ids),
        Notification.user_id == user_id
    ).all()
    
    for notification in notifications:
        notification.read = True
    
    db.session.commit()
    
    return jsonify({
        'message': f'{len(notifications)} notifications marked as read',
        'unread_count': Notification.query.filter_by(user_id=user_id, read=False).count()
    }), 200

@api_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    user_id = get_jwt_identity()
    
    # Get notification
    notification = Notification.query.get_or_404(notification_id)
    
    # Verify ownership
    if notification.user_id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    # Delete notification
    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({
        'message': 'Notification deleted',
        'unread_count': Notification.query.filter_by(user_id=user_id, read=False).count()
    }), 200
