from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)  # AA, AB, PB, etc.
    origin = db.Column(db.String(100))
    altitude = db.Column(db.String(50))
    processing = db.Column(db.String(50))
    moisture_level = db.Column(db.Float)
    cupping_notes = db.Column(db.Text)
    available_quantity = db.Column(db.Float)  # in kg
    price_per_kg = db.Column(db.Float)
    harvest_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(200)) 
    
    # Relationships
    orders = db.relationship('Order', backref='product', lazy=True)