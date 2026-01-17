from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from database import db
from enum import Enum
from datetime import datetime
import re



class UserRole(Enum):
    REGULAR="regular"
    CELEBRITY="celebrity"
    CELEBRITY_CHEF="celebrity_chef"

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)

    #Columns username,location,role,created_at,last_active
    username=Column(String(80), unique=True, nullable=False, index=True)
    location = Column(String(100), nullable=False, index=True)  
    role = Column(Enum(UserRole), nullable=False, default=UserRole.REGULAR)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    last_active = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    #relationships between each one
    cookbook = db.relationship('Cookbook', backref='owner', uselist=False, cascade='all, delete-orphan', lazy=True)
    recipes = db.relationship('Recipe', backref='creator', cascade='all, delete-orphan', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', cascade='all, delete-orphan', lazy='dynamic')
    likes = db.relationship('Like', backref='user', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, username, location, role=UserRole.REGULAR):
        """
        Initialize user and auto-create empty cookbook
        Requirement: User must be able to create only one cookbook
        """
        self.username = username
        self.location = location
        self.role = role
    