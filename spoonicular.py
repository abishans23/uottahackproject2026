from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from urrlib.parse import unquote

app = Flask(__name__)

API_KEY = os.getenv("SPOONACULAR_API_KEY")

@app.route('/home', methods=['GET'])
def home():
    render_template("recipes.html", recipes = [], search_query = "")


def getURL(filter):
    print()