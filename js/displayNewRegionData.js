'use strict';

var path = 'https://theseanfraser.github.io/ontario-arrival-departure-dates/media/lists/20_YEARS/spring/';
var selectRegionButton = document.getElementById("selectRegionButton");
var region_response;
var date_list_response, date_list_json;

function populateDatesInTable(region_response)
{
    var region_code = region_response[document.getElementById("regionSelector").value];
	var source = path + region_code + '.json';
	console.log(source);

	fetch(source)
        .then(response => response.json())
        .then(text => date_list_response = text)
        .then((response) => {
            addTable();
            });
}

function addTable(data){
    var tbody = document.getElementById("date_list_body");

    // Add each row of the data to its own table element
    for(var i = 0; i < date_list_response.length; i++){
        var tr = document.createElement("tr");
        var td_date = document.createElement("td");
        var td_species = document.createElement("td");
        var date = date_list_response[i][0]
        var species = date_list_response[i][1];
        td_date.textContent = date;
        td_date.value = date;
        td_species.textContent = species;
        td_species.value = species;
        tr.appendChild(td_date);
        tr.appendChild(td_species)
        tbody.appendChild(tr)
    }
}

selectRegionButton.onclick = function() {
	console.log("Button clicked");
	var region = document.getElementById("regionSelector").value;

    // Clear the table for the new data
	var table = document.getElementById("date_list_body");
	table.innerHTML = "";

	fetch('https://theseanfraser.github.io/ontario-arrival-departure-dates/res/regions_complete.json')
	.then(response => response.json())
    .then(text => region_response = text)
    .then((response) => {
        populateDatesInTable(region_response);
        });

};

