var regionListResponse;
var torontoListResponse;

fetch('https://numbirds.ca/ontario-arrival-departure-dates/res/species_to_code.json')
	.then(response => response.json())
    .then(text=> regionListResponse = text)
    .then((response) => {
        this.updateSelectorList();
 		});


function updateSelectorList()
{
    var selector = document.getElementById("speciesSelector");

	for(var i = 0; i < Object.keys(regionListResponse).length; i++){
	    var opt = Object.keys(regionListResponse)[i];
	    var el = document.createElement("option");
	    el.textContent = opt;
        el.value = opt;
        selector.appendChild(el);
	}

}