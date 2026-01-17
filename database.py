from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import *
from enum import Enum as PyEnum
from enum import Enum

db = SQLAlchemy()

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
    description = Column(Text, nullable=True)
    
    def __init__(self, name, description=None):
        """Initialize cookbook with name and optional description"""
        self.name = name
        self.description = description

class UserRole(PyEnum):
    REGULAR="regular"
    CELEBRITY="celebrity"
    CELEBRITY_CHEF="celebrity_chef"

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    # Columns username,location,role,created_at,last_active
    username = Column(String(80), unique=True, nullable=False, index=True)
    password = Column(String(80), nullable=False)
    # role = Column(PyEnum(UserRole), nullable=False, default=UserRole.REGULAR)

    # relationships between cookbook
    cookbook = db.relationship('Cookbook', backref='owner', uselist=False, cascade='all, delete-orphan', lazy=True)

    def __init__(self, username, password, role=UserRole.REGULAR):
        """
        Initialize user and auto-create empty cookbook
        Requirement: User must be able to create only one cookbook
        """
        self.username = username
        self.password = password
        # self.role = role

db = SQLAlchemy()

def init_db(app):

    # Connect db to Flask app (reads DATABASE_URI from config)
    db.init_app(app)
    
    # Import all models to register them with SQLAlchemy
    # This MUST happen AFTER db.init_app() but BEFORE db.create_all()
    with app.app_context():  
        # Create all tables in the database
        # This looks at all classes that inherit from db.Model
        # and creates their corresponding database tables
        db.create_all()
        
        print("Database initialized successfully!")
        print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print(f"Registered tables: {list(db.metadata.tables.keys())}")

def drop_all_tables(app):
    """
    WARNING: This deletes ALL data!
    Use only in development for resetting database
    """
    with app.app_context():
        db.drop_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

with app.app_context():
    # Create dummy data
    test_user = User(username="Gordon Ramsay", password="password123", role=UserRole.CELEBRITY_CHEF)
    db.session.add(test_user)
    db.session.commit() 

    # NOW you can query
    user = User.query.filter_by(username="Gordon Ramsay", password="password123").first()
    
    if user:
        print(f"--- SUCCESS ---")
        print(f"Found User: {user.username}")
        print(f"Role: {user.role.value}")
        print(f"Password: {user.password}")
    else:
        print("User not found.")

    # # Check if the cookbook was auto-created
    # retrieved_user = User.query.filter_by(username="ChefJoy").first()
    # print(f"User: {retrieved_user.username}")
    # print(f"Cookbook linked: {retrieved_user.cookbook.name}")