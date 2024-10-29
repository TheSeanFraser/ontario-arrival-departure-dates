'use strict';

var path = 'https://numbirds.ca/ontario-arrival-departure-dates/media/lists/20_YEARS/';
var selectRegionButton = document.getElementById("selectRegionButton");
var region_response;
var date_list_response, date_list_json;

function populateDatesInTable(region_response)
{
    var region_code = region_response[document.getElementById("regionSelector").value];
	var spring_source = path + "/spring/"+ region_code + '.json';
	var fall_source = path + "/fall/"+ region_code + '.json';

	fetch(spring_source)
        .then(response => response.json())
        .then(text => date_list_response = text)
        .then((response) => {
            addSpringTable();
            });

    fetch(fall_source)
        .then(response => response.json())
        .then(text => date_list_response = text)
        .then((response) => {
            addFallTable();
            });
}

function addSpringTable(data){
    var tbody = document.getElementById("spring_date_list_body");

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

function addFallTable(data){
    var tbody = document.getElementById("fall_date_list_body");

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

var regionSelect = document.getElementById("regionSelector");
regionSelect.onchange = function (){updateLists()};
function updateLists() {
    console.log("Button clicked");
	var region = document.getElementById("regionSelector").value;

    // Clear the tables for the new data
	var table = document.getElementById("spring_date_list_body");
	table.innerHTML = "";
	table = document.getElementById("fall_date_list_body");
	table.innerHTML = "";

	fetch('https://numbirds.ca/ontario-arrival-departure-dates/res/regions_complete.json')
	.then(response => response.json())
    .then(text => region_response = text)
    .then((response) => {
        populateDatesInTable(region_response);
        });
}
