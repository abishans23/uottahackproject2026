const selectedOption = document.getElementById("op");
const btnSelect = document.getElementById("btn");
const loader = document.getElementById("pender")
const textInput = document.getElementById("txt");

function changeFilter(){
    const val = selectedOption.value;

    if(val === "ingredient"){
        textInput.placeholder = "e.g  pickles, chocolate"
    }
    else if(val === "cuisine"){
        textInput.placeholder = "e.g Italian or Mexican"
    }
    else if(val === "diet"){
        textInput.placeholder = "e.g vegan or keto"
    }
    else if(val === "intolerance"){
        textInput.placeholder = "e.g lactose or gluten"
    }
    else{
        textInput.placeholder = "e.g  rice and curry or mango sticky rice"
    }
}

async function loadQuery(){
    loader.innerText = "Loading....."
    const query = textInput.value; 
    const filterType = selectedOption.value;

    if(!query.trim()){
        loader.innerText = "Please enter a search term";
        return;
    }

    try{
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                filter: filterType
            })
        });

        if(!response.ok){
            throw new Error('response is bad = ' + response);
        }

        const data = await response.json();
        loader.innerText = "";
        displayRecipes(data, filterType);

    }catch(err){
        loader.innerText = "Something went wrong: " + err.message;
        console.error(err);
    }
}

function displayRecipes(data, filterType){
    const recipeHolder = document.getElementById("recipe-holder");
    recipeHolder.innerHTML = "";
    
    const recipes = filterType === "ingredient" ? data : data.results;
    
    if(!recipes || recipes.length === 0){
        recipeHolder.innerHTML = "<p>No recipes found. Try a different search!</p>";
        return;
    }

    recipes.forEach(recipe => {
        const recipeCard = document.createElement('div');
        recipeCard.id = "recipe-template";        
        const title = recipe.title;
        const image = recipe.image;
        const id = recipe.id;
        
        recipeCard.innerHTML = `
            <img id="food-img" src="${image}">\n
            <div id="food-desc">${title}</div>\n
            <a href="https://spoonacular.com/recipes/${title.replace(/\s+/g, '-').toLowerCase()}-${id}" target="_blank" id="link">View Recipe</a>
        `;
        
        recipeHolder.appendChild(recipeCard);
    });
}

changeFilter()

selectedOption.addEventListener("change", changeFilter);
btnSelect.addEventListener("click", loadQuery);