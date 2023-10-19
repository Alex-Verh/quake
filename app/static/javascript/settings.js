document.addEventListener("DOMContentLoaded",  () => {

    // Settings Range Sliders //
    document.querySelectorAll(".settings-block__slider").forEach((element, index) => {
        element.addEventListener("input", () => {
            if (index < 2) {
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = element.value + "°"; 
            } else if (index < 3){
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = element.value + "%"; 
            } else if (element.value == 0) {
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = "OFF"; 
            } else {
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = "ON"; 
            }
        })
    });
});