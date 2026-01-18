const selButton = document.getElementById("btn");

function saveInfo(){

    const nameField = document.getElementById("name")
    console.log(nameField.value);
}
saveInfo()
selButton.addEventListener("onClick", saveInfo);