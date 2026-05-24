import os
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from database import init_db

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'fallback_default_secret_key')

    # Initialize database
    init_db()

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.booking import booking_bp
    from routes.maintenance import maintenance_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def index():
        if 'user_id' in session:
            role = session.get('role')
            return redirect(url_for(f'dashboard.{role}_dashboard'))
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
