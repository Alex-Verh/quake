document.addEventListener("DOMContentLoaded",  () => {

    const temperatureChart = document.querySelector("#temperature-chart");
    const humidityChart = document.querySelector("#humidity-chart");

    // Create Chart Function
    const createDiagram = (divBlock, labels, series) => {
        var elem = new Chartist.Line(divBlock, 
            {
                labels: labels,
                series: series,
            }, 
            {
                width: "100%",
                height: "100%",
                low: 0,
                showArea: true,
                fullWidth: true,
            },
        ); 

        return elem;
    }

    // History Parameters' Dropdowns
    document.addEventListener("click", (e) => {
        const historyParameter = e.target.closest(".history-parameter");
        if (historyParameter) {
            const historyParameterArrow = historyParameter.querySelector("img[alt='Arrow']");
            const historyAnalytics =  historyParameter.nextElementSibling;


            historyAnalytics.classList.toggle("none");
            if (historyAnalytics.firstElementChild === temperatureChart) {
                var tempCht = createDiagram(temperatureChart, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [[29, 30, 15, 10, 0]]);
            } else if (historyAnalytics.firstElementChild === humidityChart) {
                var humidityCht = createDiagram(humidityChart, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [[81, 65, 15, 98, 0]]);
            }

            historyParameterArrow.style.transform = historyParameterArrow.style.transform === "rotate(180deg)" ? "rotate(0deg)" : "rotate(180deg)";
        }
    })

});