from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()
app = Flask(__name__)
app.secret_key = 'secretkey'

API_KEY = os.getenv("SPOONACULAR_API_KEY")
DATABASE = 'users.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('SELECT username FROM users WHERE username = ?', ('demo',))
    if not cursor.fetchone():
        hashed_password = generate_password_hash('password123')
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                      ('demo', hashed_password))
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_user_id(username):
    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user['id'] if user else None

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

def save_recipe(user_id, name, ingredients, instructions, image_path):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO recipes (user_id, name, ingredients, instructions, image_path) VALUES (?, ?, ?, ?, ?)',
            (user_id, name, ingredients, instructions, image_path)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving recipe: {e}")
        conn.close()
        return False

def get_user_recipes(user_id):
    conn = get_db_connection()
    recipes = conn.execute(
        'SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    return recipes

def get_recipe_by_id(recipe_id, user_id):
    conn = get_db_connection()
    recipe = conn.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (recipe_id, user_id)
    ).fetchone()
    conn.close()
    return recipe

def delete_recipe(recipe_id, user_id):
    conn = get_db_connection()
    try:
        recipe = conn.execute(
            'SELECT image_path FROM recipes WHERE id = ? AND user_id = ?',
            (recipe_id, user_id)
        ).fetchone()
        
        if recipe and recipe['image_path']:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], recipe['image_path'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        conn.execute('DELETE FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting recipe: {e}")
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

@app.route('/save-recipe', methods=["POST"])
@login_required
def save_recipe_route():
    try:
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        
        if not name or not ingredients or not instructions:
            return jsonify({"error": "Missing required fields"}), 400
        
        user_id = get_user_id(session['user'])
        if not user_id:
            return jsonify({"error": "User not found"}), 404
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{user_id}_{name}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename
        
        # Save recipe to database
        if save_recipe(user_id, name, ingredients, instructions, image_path):
            return jsonify({"success": True, "message": "Recipe saved successfully!"})
        else:
            return jsonify({"error": "Failed to save recipe"}), 500
            
    except Exception as e:
        print(f"Error in save_recipe_route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/library', methods=["GET"])
@login_required
def library():
    user_id = get_user_id(session['user'])
    recipes = get_user_recipes(user_id)
    
    # Convert recipes to list of dicts
    recipes_list = []
    for recipe in recipes:
        recipes_list.append({
            'id': recipe['id'],
            'name': recipe['name'],
            'ingredients': recipe['ingredients'],
            'instructions': recipe['instructions'],
            'image_path': recipe['image_path'],
            'created_at': recipe['created_at']
        })
    
    return render_template("myCookBook.html", recipes=recipes_list)

@app.route('/get-recipes', methods=["GET"])
@login_required
def get_recipes():
    try:
        user_id = get_user_id(session['user'])
        recipes = get_user_recipes(user_id)
        
        # Convert recipes to list of dicts
        recipes_list = []
        for recipe in recipes:
            recipes_list.append({
                'id': recipe['id'],
                'name': recipe['name'],
                'ingredients': recipe['ingredients'].split(', '),
                'instructions': recipe['instructions'],
                'image_path': recipe['image_path'],
                'created_at': recipe['created_at']
            })
        
        return jsonify({"recipes": recipes_list})
    except Exception as e:
        print(f"Error getting recipes: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete-recipe/<int:recipe_id>', methods=["DELETE"])
@login_required
def delete_recipe_route(recipe_id):
    try:
        user_id = get_user_id(session['user'])
        if delete_recipe(recipe_id, user_id):
            return jsonify({"success": True, "message": "Recipe deleted successfully!"})
        else:
            return jsonify({"error": "Failed to delete recipe"}), 500
    except Exception as e:
        print(f"Error deleting recipe: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/like-recipe', methods=["POST"])
@login_required
def like_recipe():
    try:
        data = request.json
        title = data.get('title')
        image_url = data.get('image')
        recipe_link = data.get('link')
        
        if not title:
            return jsonify({"error": "Recipe title is required"}), 400
        
        user_id = get_user_id(session['user'])
        if not user_id:
            return jsonify({"error": "User not found"}), 404
        
        # Save with null ingredients/instructions and store the external image URL
        # We'll store the link in the instructions field temporarily
        ingredients = "From Spoonacular - see link for details"
        instructions = f"View full recipe at: {recipe_link}" if recipe_link else "External recipe"
        
        # Store the image URL directly (external URL)
        if save_recipe(user_id, title, ingredients, instructions, image_url):
            return jsonify({"success": True, "message": "Recipe saved to your cookbook!"})
        else:
            return jsonify({"error": "Failed to save recipe"}), 500
            
    except Exception as e:
        print(f"Error in like_recipe: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port="5000")