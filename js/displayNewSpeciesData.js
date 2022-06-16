'use strict';

var path = 'https://theseanfraser.github.io/ontario-arrival-departure-dates/media/maps/spring/';
var selectSpeciesButton = document.getElementById("selectSpeciesButton");

selectSpeciesButton.onclick = function() {
	console.log("Button clicked");
	var species = document.getElementById("speciesSelector").value;

    var map_img = document.getElementById("map_img");
    map_img.src = path + species + ".png";

};

