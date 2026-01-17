
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

       function loadQuery(){
            loader.innerText = "Loading....."
            const query = document.getElementById("txt");

            try{
                const f = 4/0
            }catch(err){
                loader.innerText = "Something went wrong"
            }

       }
       changeFilter()

       selectedOption.addEventListener("change", changeFilter);
       btnSelect.addEventListener("click", loadQuery);
       
