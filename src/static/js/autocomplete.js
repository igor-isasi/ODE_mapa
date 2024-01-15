export function autocomplete(inp, arr) {
    let currentFocus;
    inp.addEventListener("input", function() {
        let val = this.value;
        cerrarListaAutocomplete();
        if (!val) { return false;}
        currentFocus = -1;
        let a = document.createElement("DIV");
        a.setAttribute("id", "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (let i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                let b = document.createElement("DIV");
                b.innerHTML = "<strong>" + convertirMayuscula(arr[i].substr(0, val.length)) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + convertirMayuscula(arr[i]) + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    cerrarListaAutocomplete();
                });
            a.appendChild(b);
          }
        }
    });
    inp.addEventListener("keydown", function(e) {
        let x = document.getElementById("autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) {
            currentFocus--;
          	addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });
    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function cerrarListaAutocomplete() {
        let listaAutocomplete = document.getElementById("autocomplete-list");
        if (listaAutocomplete != null) {
            listaAutocomplete.parentNode.removeChild(listaAutocomplete);
        }
    }
    document.addEventListener("click", function () {
        cerrarListaAutocomplete();
    });
} 

export function convertirMayuscula(palabra) {
	let letraMayus = palabra.charAt(0).toUpperCase();
	let palabraMayus = letraMayus + palabra.slice(1);
	return palabraMayus	
}

export function convertirMinuscula(palabra) {
	let letraMinus = palabra.charAt(0).toLowerCase();
	let palabraMinus = letraMinus + palabra.slice(1);
	return palabraMinus;
}
