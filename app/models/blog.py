from app import db
from datetime import datetime
from slugify import slugify

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    summary = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    featured_image = db.Column(db.String(200))
    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    meta_description = db.Column(db.String(160))
    meta_keywords = db.Column(db.String(160))
    
    author = db.relationship('User', backref='blog_posts')