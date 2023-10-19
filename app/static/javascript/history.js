document.addEventListener("DOMContentLoaded",  () => {

    document.addEventListener("click", (e) => {
        const historyParameter = e.target.closest(".history-parameter");
        if (historyParameter) {
            const historyParameterArrow = historyParameter.querySelector("img[alt='Arrow']");

            historyParameter.nextElementSibling.classList.toggle("none");
            historyParameterArrow.style.transform = historyParameterArrow.style.transform === "rotate(180deg)" ? "rotate(0deg)" : "rotate(180deg)";
        }
    })

});