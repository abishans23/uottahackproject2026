from data.database import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
import json

class Recipe(db.Model):
    __tablename__ = "recipes"

    # FIXED: Added Integer type and primary_key flag
    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False, index=True)
    ingredients = Column(Text, nullable=False)  # Store as JSON string
    instructions = Column(Text, nullable=False)
    
    # Foreign Keys - Linked to 'users' and 'cookbooks' table names
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    cookbook_id = Column(Integer, ForeignKey('cookbooks.id'), nullable=False, index=True)
    
    like_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps (using utcnow is better for global apps)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='recipe', cascade='all, delete-orphan', lazy='dynamic')
    likes = db.relationship('Like', backref='recipe', cascade='all, delete-orphan', lazy='dynamic')
    
    def __init__(self, title, ingredients, instructions, creator_id, cookbook_id):
        self.title = title
        # If ingredients is a list, convert to JSON string automatically
        if isinstance(ingredients, list):
            self.ingredients = json.dumps(ingredients)
        else:
            self.ingredients = ingredients
            
        self.instructions = instructions
        self.creator_id = creator_id
        self.cookbook_id = cookbook_id