const selButton = document.getElementById("btn");

function saveInfo(){

    const nameField = document.getElementById("name")
    console.log(nameField.value);

    const ingredientField = document.getElementById("ingredients")
    console.log(ingredientField.value);

    const instructionField = document.getElementById("instructions")
    console.log(instructionField.value)

    const ingredients = ingredientField.value.split(', ')

    const obj = {
        "name":nameField.value, "ingredients":ingredients, "instructions":instructionField.value
    }

    return obj
}
saveInfo()
selButton.addEventListener("click", saveInfo);