
        const selectedOption = document.getElementById("op");
        const btnSelect = document.getElementById("btn");
        const loader = document.getElementById("pender")
        const textInput = document.getElementById("txt");
        const filterType = selectedOption.value;

        

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
            const query = document.getElementById("txt");

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
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                loader.innerText = "";
                displayRecipes(data, filterType);

            }catch(err){
                loader.innerText = "Something went wrong: " + err.message;
                console.error(err);
            }

       }
       changeFilter()

       selectedOption.addEventListener("change", changeFilter);
       btnSelect.addEventListener("click", loadQuery);
       
