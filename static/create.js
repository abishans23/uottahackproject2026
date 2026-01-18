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

function saveInfo() {
    const nameField = document.getElementById("name");
    const ingredientField = document.getElementById("ingredients");
    const instructionField = document.getElementById("instructions");
    
    const ingredients = ingredientField.value.split(', ');


    const obj = {
        "name": nameField.value,
        "ingredients": ingredients,
        "instructions": instructionField.value,
        "image": uploadedImage
    }

    console.log(obj);
    return obj;
}

selButton.addEventListener("click", saveInfo);