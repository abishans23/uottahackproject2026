from database import db
from datetime import datetime
from sqlalchemy import *

class Comment(db.Model):
    """
    Comment model - Users can comment on recipes
    Requirement: User must be able to comment on a recipe
    """
    __tablename__ = 'comments'
    
    # Primary Key
    id = Column(Integer, primary_key=True)
    
    # Comment Content
    content = Column(Text, nullable=False)
    
    # Foreign Keys
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __init__(self, content, recipe_id, user_id):
        """Initialize comment with content, recipe, and user"""
        self.content = content
        self.recipe_id = recipe_id
        self.user_id = user_id