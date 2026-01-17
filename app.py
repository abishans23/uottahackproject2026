from flask import Flask, render_template, request
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route('/home', methods=['GET'])
def home():
    render_template("recipes.html", recipes = [], search_query = "")

@app.route('/search', methods=["GET", "POST"])
def search():
    return

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)