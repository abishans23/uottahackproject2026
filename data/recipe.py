from database import db
from datetime import datetime
from sqlalchemy import *
import json

class Recipe(db.Model):
    __tablename__="recipes"

    id=Column()

    title = Column(String(200), nullable=False, index=True)
    ingredients = Column(Text, nullable=False)  # Store as JSON string
    instructions = Column(Text, nullable=False)
    
    # Foreign Keys
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    cookbook_id = Column(Integer, ForeignKey('cookbooks.id'), nullable=False, index=True)
    
    # Denormalized counter for performance
    like_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    # One-to-Many: Recipe has many comments
    comments = db.relationship('Comment', backref='recipe', cascade='all, delete-orphan', lazy='dynamic')
    
    # One-to-Many: Recipe has many likes
    likes = db.relationship('Like', backref='recipe', cascade='all, delete-orphan', lazy='dynamic')
    
    def __init__(self, title, ingredients, instructions, creator_id, cookbook_id):
        self.title = title
        self.ingredients=ingredients
        self.instructions = instructions
        self.creator_id = creator_id
        self.cookbook_id = cookbook_id
        