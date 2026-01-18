from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



def init_db(app):
   
    
    # Connect db to Flask app (reads DATABASE_URI from config)
    db.init_app(app)
    
    # Import all models to register them with SQLAlchemy
    # This MUST happen AFTER db.init_app() but BEFORE db.create_all()
    with app.app_context():
        # Import models here so SQLAlchemy knows about them
        from user import User, UserRole
        from cookbook import Cookbook
        from recipe import Recipe
        from comment import Comment
        from like import Like
        
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
        


