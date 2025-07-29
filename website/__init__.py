
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Secure configuration using environment variables
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+mysqlconnector://root:@localhost/user'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enhanced session security
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to False for local testing (HTTP)
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = int(os.environ.get('SESSION_TIMEOUT', 1800))  # Use env variable
    
    # CSRF Protection
    csrf = CSRFProtect(app)
    
    db.init_app(app)


    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Subject, Grade
    with app.app_context():
        db.create_all()  # Remove db.drop_all() after first run

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'  # Enhanced session protection
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app



def create_database(app):
    db.create_all(app=app)
    print('Created Database!')




