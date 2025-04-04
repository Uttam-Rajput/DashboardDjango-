google.charts.load('current', { packages: ['corechart', 'geochart'] });
google.charts.setOnLoadCallback(fetchData);

function fetchData() {
    fetch('/api/get_chart_data/')  // Call Django API
        .then(response => response.json())
        .then(jsonData => {
            drawCharts(jsonData.data);
        });
}

function drawCharts(data) {
    let chartData = [['Country', 'Intensity']];
    data.forEach(row => {
        chartData.push([row.country, row.intensity]);
    });

    var dataTable = google.visualization.arrayToDataTable(chartData);

    var options = { title: 'Intensity by Country' };
    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(dataTable, options);
}
