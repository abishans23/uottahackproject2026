from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
# bcrypt = Bcrypt(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
# app.config['SECRET_KEY'] = 'database123'

db = SQLAlchemy()

def init_db(app):
   
    # Connect db to Flask app (reads DATABASE_URI from config)
    db.init_app(app)
    
    # Import all models to register them with SQLAlchemy
    # This MUST happen AFTER db.init_app() but BEFORE db.create_all()
    with app.app_context():
        class User(db.Model, UserMixin):
            __tablename__ = "accounts"
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(20), nullable=False, unique=True)
            password = db.Column(db.String(80), nullable=False)

            def __init__(self, id, username, password):
                self.id = id
                self.username = username
                self.password = password
        
        # Create all tables in the database
        # This looks at all classes that inherit from db.Model
        # and creates their corresponding database tables
        db.create_all()
        
        print("Database initialized successfully!")
        print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print(f"Registered tables: {list(db.metadata.tables.keys())}")








login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


API_KEY = os.getenv("API_KEY")

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/loggedin')
    return render_template('index.html', form=form)

@app.route('/search', methods=["GET", "POST"])
def search():
    return

@app.route('/loggedin', methods=["GET", "POST"])
def home():
    return render_template("loggedin.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8000")