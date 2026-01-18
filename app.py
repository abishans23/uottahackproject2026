from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

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
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = get_user(username)
        
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port="5500")