from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """Define UserMixin for Flask Login to Manage User sessions"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_recycler = db.Column(db.Boolean, default=False)
    waste_posts = db.relationship('WastePost', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WastePost(db.Model):
    """Model for tracking waste details"""
    __tablename__ = 'waste_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Other fields like GPS coordinates could be added here
    
    def __repr__(self):
        return f"<WastePost '{self.title}'>"


class RecyclerView(db.Model):
    """Model to track whick recycler views waste posts"""
    __tablename__ = 'recycler_views'

    id = db.Column(db.Integer, primary_key=True)
    recycler_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    waste_post_id = db.Column(db.Integer, db.ForeignKey('waste_posts.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RecyclerView by {self.recycler_id} on post {self.waste_post_id}>"
