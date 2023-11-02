from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# import other necessary modules

# Initialize the database
db = SQLAlchemy()

# Initialize the login manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configure your app, e.g. secret key, database URI, etc.
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://deno:password@localhost/climatehackathon'

    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register the auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)
    
    # ... Register other blueprints and configure other parts of the app
    
    return app
