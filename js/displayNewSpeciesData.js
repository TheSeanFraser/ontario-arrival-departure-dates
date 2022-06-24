'use strict';

var spring_path = 'https://theseanfraser.github.io/ontario-arrival-departure-dates/media/maps/spring/';
var fall_path = 'https://theseanfraser.github.io/ontario-arrival-departure-dates/media/maps/fall/';
var selectSpeciesButton = document.getElementById("selectSpeciesButton");

selectSpeciesButton.onclick = function() {
	console.log("Button clicked");
	var species = document.getElementById("speciesSelector").value;

    var spring_map_img = document.getElementById("spring_map_img");
    var fall_map_img = document.getElementById("fall_map_img");

    spring_map_img.src = spring_path + species + ".png";
    fall_map_img.src = fall_path + species + ".png";

};

