from database import db
from datetime import datetime
from sqlalchemy import *

class Like(db.Model):
    """
    Like model - Users can like recipes
    Requirement: User must be able to like a recipe
    """
    __tablename__ = 'likes'
    
    # Primary Key
    id = Column(Integer, primary_key=True)
    
    # Foreign Keys
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
    # Ensure a user can only like a recipe once
    __table_args__ = (
        UniqueConstraint('recipe_id', 'user_id', name='unique_user_recipe_like'),
    )
    
    def __init__(self, recipe_id, user_id):
        """Initialize like with recipe and user"""
        self.recipe_id = recipe_id
        self.user_id = user_id
    