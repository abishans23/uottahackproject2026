from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = 'secretkey'

API_KEY = os.getenv("SPOONACULAR_API_KEY")
DATABASE = 'users.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create demo user if it doesn't exist
    cursor.execute('SELECT username FROM users WHERE username = ?', ('demo',))
    if not cursor.fetchone():
        hashed_password = generate_password_hash('password123')
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                      ('demo', hashed_password))
    
    conn.commit()
    conn.close()

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = get_db_connection()
    hashed_password = generate_password_hash(password)
    try:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                    (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('recipes'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('recipes'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = get_user(username)
        
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('recipes'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters', 'error')
        else:
            if create_user(username, password):
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already taken', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/recipes')
@login_required
def recipes():
    return render_template("recipes.html")

@app.route('/search', methods=["POST"])
@login_required
def search():
    try:
        data = request.json
        query = data.get("query")
        filter_type = data.get("filter")
        
        print(f"Query: {query}")  
        print(f"Filter: {filter_type}")  
        print(f"API Key: {API_KEY}")  

        BASE_URL = "https://api.spoonacular.com/recipes/"
        params = {"apiKey": API_KEY} 

        if filter_type == "ingredient":
            params["ingredients"] = query
            url = BASE_URL + "findByIngredients"
        else:
            url = BASE_URL + "complexSearch"
            if filter_type == "cuisine":
                params["cuisine"] = query
            elif filter_type == "diet":
                params["diet"] = query
            elif filter_type == "intolerance":
                params["intolerances"] = query
            else:
                params["query"] = query
        
        print(f"URL: {url}") 
        print(f"Params: {params}") 
        
        response = requests.get(url, params=params)
        
        print(f"Response status: {response.status_code}") 
        print(f"Response: {response.text}")  
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "API request failed"}), 500
            
    except Exception as e:
        print(f"ERROR: {e}")  
        return jsonify({"error": str(e)}), 500

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    return render_template("createRecipe.html")

@app.route('/library', methods=["GET", "POST"])
@login_required
def library():
    return render_template("myCookBook.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port="5000")