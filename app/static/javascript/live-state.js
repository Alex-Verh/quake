document.addEventListener("DOMContentLoaded",  () => {
	var socket = io();
    socket.on('connect', () => {
        console.log("connected")
    });
	socket.on('sensors', sensors => {
		console.log(sensors)
		document.querySelector("#temperature").innerHTML = sensors["temperature"];
		document.querySelector("#humidity").innerHTML = sensors["humidity"] + "%";
		document.querySelector("#smoke").innerHTML = bool_to_msg(sensors["smoke"], "smoke");
		document.querySelector("#earthquake").innerHTML = bool_to_msg(sensors["earthquake"], "farthquake");
		document.querySelector("#flammable_gas").innerHTML = bool_to_msg(sensors["flammable_gas"], "flammable gas");
		document.querySelector("#flame").innerHTML = bool_to_msg(sensors["flame"], "fire");
		document.querySelector("#time").innerHTML = sensors["time"];
	});
});

function bool_to_msg(bool, name) {
	if (bool) {
		return `${name} detected!`
	} else {
		return `No ${name} detected`
	}
}
