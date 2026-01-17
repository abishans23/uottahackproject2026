from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("SPOONACULAR_API_KEY")


@app.route('/')
def recipe():
    return render_template("recipes.html")

@app.route('/search', methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True, port = "5500")