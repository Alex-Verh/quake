import {fetchTheme} from "./general.js";

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

    // Function to update a chart
    function updateChart(chart, data, length) {
        while (data.labels.length > length) {
            data.labels.shift();
        }
        while (data.series[0].length > length) {
            data.series[0].shift();
        }
        chart.update(data);
    }
    
    // Reference to the chards
    let tempCht = createDiagram(temperatureChart, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [[29, 30, 15, 10, 0]]);
    let humidityCht = createDiagram(humidityChart, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [[81, 65, 15, 98, 0]]);

    // History Parameters' Dropdowns
    document.addEventListener("click", (e) => {
        const historyParameter = e.target.closest(".history-parameter");
        if (historyParameter) {
            const historyParameterArrow = historyParameter.querySelector("img[alt='Arrow']");
            const historyAnalytics =  historyParameter.nextElementSibling;


            historyAnalytics.classList.toggle("none");
            if (historyAnalytics.firstElementChild === temperatureChart) {
                // var tempCht = createDiagram(temperatureChart, ['1', 'xx', 'Wed', 'Thu', 'Fri'], [[29, 30, 15, 10, 0]]);
            } else if (historyAnalytics.firstElementChild === humidityChart) {
                // var humidityCht = createDiagram(humidityChart, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [[81, 65, 15, 98, 0]]);
            }

            historyParameterArrow.style.transform = historyParameterArrow.style.transform === "rotate(180deg)" ? "rotate(0deg)" : "rotate(180deg)";
        }
    })

    var socket = io();
    socket.on('connect', () => {
        console.log("connected");
    });
    socket.on('history', history_data => {
        console.log(history_data);
        // console.log(data['avg_humidity']);
        const time_labels = history_data['timestamp'].map(timestamp => {
            const parts = timestamp.split(' ')[1].split(':');
            return parts[0] + ':' + parts[1];
        });

        let data = {
            labels: time_labels,
            series: [history_data['avg_temperature']]
        };
        updateChart(tempCht, data, 10);

        data.series = [history_data['avg_humidity']];
        updateChart(humidityCht, data, 20);
    });

    fetchTheme();
});