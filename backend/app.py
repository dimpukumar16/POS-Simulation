import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
from models.user import db
from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.checkout import checkout_bp
from routes.reports import reports_bp
from routes.refunds import refund_bp
from routes.settings import settings_bp
from utils.db import init_db, seed_database

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# Debug: Print to verify keys are loaded
print(f"DEBUG: SECRET_KEY loaded: {app.config['SECRET_KEY'][:20]}...")
print(f"DEBUG: JWT_SECRET_KEY loaded: {app.config['JWT_SECRET_KEY'][:20]}...")

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_dir = os.path.join(os.path.dirname(basedir), 'database')
os.makedirs(database_dir, exist_ok=True)

# Check for MySQL configuration
mysql_uri = os.environ.get('MYSQL_URI')
if mysql_uri:
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
else:
    # Default to SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(database_dir, "pos.db")}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

# Initialize database
init_db(app)

# Seed database if empty
with app.app_context():
    from models.user import User
    if not User.query.first():
        seed_database(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(refund_bp)
app.register_blueprint(settings_bp)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    import traceback
    print(f"DEBUG: Invalid token error: {error}")
    print(f"DEBUG: Error type: {type(error)}")
    print(f"DEBUG: Traceback:")
    traceback.print_exc()
    return jsonify({'error': 'Invalid token', 'details': str(error)}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token is missing'}), 401


# Root endpoint
@app.route('/')
def index():
    return jsonify({
        'message': 'POS Simulator API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'products': '/api/products',
            'cart': '/api/cart',
            'checkout': '/api/checkout',
            'reports': '/api/reports'
        }
    })


# Debug endpoint to check headers
@app.route('/debug/headers')
def debug_headers():
    from flask import request
    return jsonify({
        'headers': dict(request.headers),
        'auth_header': request.headers.get('Authorization', 'NOT FOUND')
    })


# Health check endpoint
@app.route('/health')
def health_check():
    try:
        # Check database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'database': db_status
    })


if __name__ == '__main__':
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("\n" + "="*60)
    print("🚀 POS Simulator Backend Starting...")
    print("="*60)
    print(f"📍 Server: http://localhost:{port}")
    print(f"📁 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"🔧 Debug Mode: {debug}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
