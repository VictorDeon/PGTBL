// Callback that creates and populates a data table,
// instantiates the line chart, passes in the data and
// draws it.
function drawChartStudentsgRAT() {
  // Create the table
  var data = new google.visualization.arrayToDataTable([
    ['Grupo', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10'],
    ['Grupo 01',  0, 4, 4, 3, 3, 2, 1, 4, 4, 4],
    ['Grupo 02',  3, 2, 2, 4, 4, 2, 3, 4, 1, 2],
    ['Grupo 03',  4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    ['Grupo 04',  3, 1, 4, 4, 4 ,3, 2, 3, 4, 1],
    ['Grupo 05',  2, 0, 0, 4, 3, 4, 4, 0, 0, 1],
  ]);

  // Set chart options
  var options = {
    title: 'Pontuação por grupo: gRAT',
    legend: { position: 'top'},
    hAxis: {title: 'Pontuação',  minValue: 0, maxValue: 40, titleTextStyle: {color: '#333'}},
    vAxis: {title:'Grupos', titleTextStyle: {color: '#333'}},
    isStacked: true
  }

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.BarChart(document.getElementById('chart-students-grat'))

  // Wait for the chart to finish drawing before calling the getImageURI() method.
  google.visualization.events.addListener(chart, 'ready', function () {
    document.getElementById('png-grat').innerHTML = '<a href="' + chart.getImageURI() + '" download="gRAT_report">Download PNG</a>';
  });

  // Draw the chart
  chart.draw(data, options)
}