import requests
import os
import pprint


spoonacular_api_key = os.environ["SPOONACULAR_API_KEY"]

HEALTHY_URL = "https://api.spoonacular.com/recipes/findByNutrients"
INGREDIENTS_URL = "https://api.spoonacular.com/recipes/findByIngredients"

def makeRecipe(minProtein, filterParam):
    if filterParam == "healthy":
        url = HEALTHY_URL
        params = {
            "apiKey": spoonacular_api_key,
            "minProtein": minProtein,
            "number": 5
        }
    else:
        url = INGREDIENTS_URL
        params = {
            "apiKey": spoonacular_api_key,
            "ingredients": "chicken,rice",
            "number": 5
        }

    response = requests.get(url, params=params)
    response.raise_for_status()
    pprint.pprint(response.json())

makeRecipe(10, "healthy")
