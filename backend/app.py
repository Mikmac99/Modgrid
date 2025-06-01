from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    # Enable CORS
    CORS(app)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE_URL=os.environ.get('DATABASE_URL', 'sqlite:///modulargrid.db'),
        JWT_SECRET=os.environ.get('JWT_SECRET', 'jwt-secret-key'),
        ENCRYPTION_KEY=os.environ.get('ENCRYPTION_KEY', 'encryption-key-must-be-32-bytes-long')
    )
    
    # Register blueprints
    from app.api import modules_bp, deals_bp, watchlist_bp, monitor_bp, notifications_bp
    app.register_blueprint(modules_bp)
    app.register_blueprint(deals_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(monitor_bp)
    app.register_blueprint(notifications_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # API status route
    @app.route('/api/status')
    def status():
        return jsonify({
            'status': 'online',
            'version': '1.0.0'
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
