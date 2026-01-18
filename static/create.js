const selButton = document.getElementById("btn");
const dropZone = document.getElementById('dropZone');
let uploadedImage = null;

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.backgroundColor = '#e0e0e0';
});

dropZone.addEventListener('dragleave', (e) => {
    dropZone.style.backgroundColor = '#f9f9f9';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.backgroundColor = '#f9f9f9';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        uploadedImage = file;
        
        const reader = new FileReader();
        reader.onload = function(event) {
            dropZone.innerHTML = `
                <img src="${event.target.result}" style="max-width: 100%; max-height: 300px; border-radius: 4px;">
                <p style="margin-top: 10px; font-size: 14px;">Image uploaded: ${file.name}</p>
            `;
        };
        reader.readAsDataURL(file);
    }
});

async function saveInfo() {
    const nameField = document.getElementById("nameInput");
    const ingredientField = document.getElementById("ingredients");
    const instructionField = document.getElementById("instructions");
    
    // Validate inputs
    if (!nameField.value.trim()) {
        alert("Please enter a recipe name");
        return;
    }
    
    if (!ingredientField.value.trim()) {
        alert("Please enter ingredients");
        return;
    }
    
    if (!instructionField.value.trim()) {
        alert("Please enter instructions");
        return;
    }
    
    // Create FormData to send file and text data
    const formData = new FormData();
    formData.append('name', nameField.value);
    formData.append('ingredients', ingredientField.value);
    formData.append('instructions', instructionField.value);
    
    if (uploadedImage) {
        formData.append('image', uploadedImage);
    }
    
    try {
        // Show loading state
        selButton.disabled = true;
        selButton.textContent = "Saving...";
        
        const response = await fetch('/save-recipe', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert("Recipe saved successfully!");
            
            nameField.value = '';
            ingredientField.value = '';
            instructionField.value = '';
            uploadedImage = null;
            dropZone.innerHTML = 'Drag and drop an image here';
            
            window.location.href = '/library';
        } else {
            alert("Error saving recipe: " + (data.error || "Unknown error"));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error saving recipe: " + error.message);
    } finally {
        selButton.disabled = false;
        selButton.textContent = "Submit";
    }
}

selButton.addEventListener("click", saveInfo);