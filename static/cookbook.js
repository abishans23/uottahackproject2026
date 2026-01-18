document.addEventListener('DOMContentLoaded', loadRecipes);

async function loadRecipes() {
    try {
        const response = await fetch('/get-recipes');
        const data = await response.json();
        
        if (response.ok && data.recipes) {
            displayRecipes(data.recipes);
        } else {
            console.error('Error loading recipes:', data.error);
            alert('Error loading recipes');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading recipes');
    }
}

function displayRecipes(recipes) {
    const cookbookShelf = document.getElementById('cookbook-shelf');
    
    cookbookShelf.innerHTML = '';
    
    if (recipes.length === 0) {
        cookbookShelf.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; font-size: 18px;">No recipes yet. Create your first recipe!</p>';
        return;
    }
    
    recipes.forEach(recipe => {
        const card = createRecipeCard(recipe);
        cookbookShelf.appendChild(card);
    });
}

function createRecipeCard(recipe) {
    const card = document.createElement('div');
    card.className = 'cookbook-card';
    
    const imageSrc = recipe.image_path 
        ? `/static/uploads/${recipe.image_path}` 
        : 'https://via.placeholder.com/300x200?text=No+Image';
    
    card.innerHTML = `
        <img src="${imageSrc}" class="food-img" alt="${recipe.name}" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
        <div class="food-desc">${recipe.name}</div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <button class="view-btn" onclick="viewRecipe(${recipe.id})">View Recipe</button>
            <button class="delete-btn" onclick="deleteRecipe(${recipe.id})">Delete</button>
        </div>
    `;
    
    return card;
}

function viewRecipe(recipeId) {
    fetch('/get-recipes')
        .then(response => response.json())
        .then(data => {
            const recipe = data.recipes.find(r => r.id === recipeId);
            if (recipe) {
                showRecipeModal(recipe);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading recipe details');
        });
}

function showRecipeModal(recipe) {
    const modal = document.createElement('div');
    modal.id = 'recipe-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;
    
    const imageSrc = recipe.image_path 
        ? `/static/uploads/${recipe.image_path}` 
        : 'https://via.placeholder.com/400x300?text=No+Image';
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background-color: rgb(216, 211, 225);
        padding: 30px;
        border-radius: 15px;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        position: relative;
    `;
    
    modalContent.innerHTML = `
        <button onclick="closeModal()" style="
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: rgb(159, 144, 166);
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 18px;
        ">×</button>
        <h2 style="margin-top: 0;">${recipe.name}</h2>
        <img src="${imageSrc}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 10px; margin-bottom: 20px;" onerror="this.src='https://via.placeholder.com/400x300?text=No+Image'">
        <h3>Ingredients:</h3>
        <ul style="line-height: 1.6;">
            ${recipe.ingredients.map(ing => `<li>${ing}</li>`).join('')}
        </ul>
        <h3>Instructions:</h3>
        <p style="white-space: pre-wrap; line-height: 1.6;">${recipe.instructions}</p>
    `;
    
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}

function closeModal() {
    const modal = document.getElementById('recipe-modal');
    if (modal) {
        modal.remove();
    }
}

async function deleteRecipe(recipeId) {
    if (!confirm('Are you sure you want to delete this recipe?')) {
        return;
    }
    
    try {
        const response = await fetch(`/delete-recipe/${recipeId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert('Recipe deleted successfully!');
            loadRecipes();
        } else {
            alert('Error deleting recipe: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting recipe: ' + error.message);
    }
}