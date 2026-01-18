from flask import Flask
from data.database import db
from data.user import User, UserRole
from data.user import User
from data.cookbook import Cookbook 
from data.recipe import Recipe
from data.comment import Comment
from data.like import Like

# 1. Setup a dummy Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Fast, temporary DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Initialize the DB with the app
db.init_app(app)

# 3. Everything must happen inside the 'app_context'
with app.app_context():
    # Create the tables
    db.create_all()

    # Create dummy data
    test_user = User(username="Gordon Ramsay", location="London", role=UserRole.CELEBRITY_CHEF)
    db.session.add(test_user)
    db.session.commit() 

    # NOW you can query
    user = User.query.filter_by(username="Gordon Ramsay",location="London").first()
    
    if user:
        print(f"--- SUCCESS ---")
        print(f"Found User: {user.username}")
        print(f"Role: {user.role.value}")
        print(f"User in: {user.location}")
    else:
        print("User not found.")


