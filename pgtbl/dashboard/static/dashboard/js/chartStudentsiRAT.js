// Callback that creates and populates a data table,
// instantiates the line chart, passes in the data and
// draws it.
function drawChartStudentsiRAT() {
  // Create the table
  var data = new google.visualization.arrayToDataTable([
    ['Aluno', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10'],
    ['13029384',  0, 4, 4, 3, 3, 2, 1, 4, 4, 4],
    ['12394956',  3, 2, 2, 4, 4, 2, 3, 4, 1, 2],
    ['11928394',  4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    ['10293945',  3, 1, 4, 4, 4 ,3, 2, 3, 4, 1],
    ['15938285',  2, 0, 0, 4, 3, 4, 4, 0, 0, 1],
  ]);

  // Set chart options
  var options = {
    title: 'Pontuação por aluno: iRAT',
    legend: { position: 'top'},
    hAxis: {title: 'Pontuação',  minValue: 0, maxValue: 40, titleTextStyle: {color: '#333'}},
    vAxis: {title:'Alunos', titleTextStyle: {color: '#333'}},
    isStacked: true
  }


  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.BarChart(document.getElementById('chart-students-irat'))

  // Wait for the chart to finish drawing before calling the getImageURI() method.
  google.visualization.events.addListener(chart, 'ready', function () {
    document.getElementById('png-irat').innerHTML = '<a href="' + chart.getImageURI() + '" download="iRAT_report">Download PNG</a>';
  });

  // Draw the chart
  chart.draw(data, options)
}