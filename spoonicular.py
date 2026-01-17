from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from urrlib.parse import unquote

app = Flask(__name__)

API_KEY = os.getenv("SPOONACULAR_API_KEY")


@app.route('/')
def recipe():
    return render_template("recipes.html")

@app.route('/search', ["POST"])
def search():
    data = request.json
    query = data.get("query")
    filter_type = data.get("filter")

    BASE_URL = "https://api.spoonacular.com/recipes/"
    params = {"apiKey": API_KEY} 

    if filter_type == "ingredients" :
        params["ingredients"] = query
        url = BASE_URL + "findByIngredients"
    
    else:
        url = BASE_URL + "complexSearch"
        if filter_type == "cuisine" :
            params["cuisine"] = query
        
        elif filter_type == "diet":
            params["diet"] = query

        elif filter_type == "intolerance":
            params["intolerance"] = query

        else:
            params["query"] = query
    

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "API request failed"}), 500

    if __name__ == "__main__":
        app.run(debug=True)
