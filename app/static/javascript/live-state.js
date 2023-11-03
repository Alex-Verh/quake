document.addEventListener("DOMContentLoaded",  () => {
	var socket = io();
    socket.on('connect', () => {
        console.log("connected")
    });
	socket.on('sensors', sensors => {
		console.log(sensors)
		document.querySelector("#temperature").innerHTML = sensors["temperature"] + "°C";
		document.querySelector("#humidity").innerHTML = sensors["humidity"] + "%";

		document.querySelector("#smoke").innerHTML = bool_to_msg(sensors["smoke"], "smoke");
		document.querySelector("#smoke").style.color = bool_to_colour(sensors["smoke"]);

		document.querySelector("#gas").innerHTML = bool_to_msg(sensors["gas"], "gas");
		document.querySelector("#gas").style.color = bool_to_colour(sensors["gas"]);

		document.querySelector("#flame").innerHTML = bool_to_msg(sensors["flame"], "fire");
		document.querySelector("#flame").style.color = bool_to_colour(sensors["flame"]);

		document.querySelector("#earthquake").innerHTML = bool_to_msg(sensors["earthquake"], "earthquake");
		document.querySelector("#earthquake").style.color = bool_to_colour(sensors["earthquake"]);

		document.querySelector("#time").innerHTML = sensors["time"].split(' ')[1];
		document.querySelector("#date").innerHTML = sensors["time"].split(' ')[0];
	});
});

function bool_to_msg(bool, name) {
	if (bool) {
		return `${name.charAt(0).toUpperCase()}${name.slice(1)} detected!`
	} else {
		return `No ${name} detected`
	}
}

function bool_to_colour(bool) {
	if (bool) {
		return "red";
	} else {
		return "green";
	}
}
