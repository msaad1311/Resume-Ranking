const myChart = new EasyPieChart(document.querySelector('.chart'), {

    barColor: '#ef1e25',
    // The color of the track for the bar, false to disable rendering.
    trackColor: '#f2f2f2',
    // The color of the scale lines, false to disable rendering.
    scaleColor: '#dfe0e0',
    // Defines how the ending of the bar line looks like. Possible values are: butt, round and square.
    lineCap: 'round',
    // Width of the bar line in px.
    lineWidth: 3,
    // Size of the pie chart in px. It will always be a square.
    size: 110,
    // Time in milliseconds for a eased animation of the bar growing, or false to deactivate.
    animate: 1000,
});