from database import db
from datetime import datetime
from sqlalchemy import *

class Cookbook(db.Model):
    """
    Cookbook model - Each user has exactly ONE cookbook
    Requirement: User must be able to create only one cookbook
    """
    __tablename__ = 'cookbooks'
    
    id = Column(Integer, primary_key=True)
    
    # Foreign Key to User (UNIQUE ensures one cookbook per user)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False, index=True)
    
    # Cookbook Information
    name = Column(String(100), nullable=False)
    description = Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    # One-to-Many: Cookbook contains many recipes
    recipes = db.relationship('Recipe', backref='cookbook', cascade='all, delete-orphan', lazy='dynamic')
    
    def __init__(self, name, description=None):
        """Initialize cookbook with name and optional description"""
        self.name = name
        self.description = description