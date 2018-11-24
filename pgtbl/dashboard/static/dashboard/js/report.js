// Load the Visualization API and the corechart package.
google.charts.load('visualization', "1", {'packages': ['corechart']});
// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChartQuestions);
google.charts.setOnLoadCallback(drawChartStudentsiRAT);
google.charts.setOnLoadCallback(drawChartStudentsgRAT);

// Callback that creates and populates a data table,
// instantiates the line chart, passes in the data and
// draws it.
function drawChartQuestions() {
  var graphic = document.getElementById('questions-data').innerHTML
  graphic = parser(graphic)
  graphic.splice(0, 0, ['Questões', 'iRAT', 'gRAT'])

  // Create the table
  var data = new google.visualization.arrayToDataTable(graphic);

  // Set chart options
  var options = {
    title: 'Quantidade de acertos por questões',
    hAxis: {title: 'Questões',  titleTextStyle: {color: '#333'}},
    vAxis: {title:'Quantidade de acertos', minValue: 0, maxValue: 50, titleTextStyle: {color: '#333'}}
  }

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.AreaChart(document.getElementById('chart-questions'))

  // Wait for the chart to finish drawing before calling the getImageURI() method.
  google.visualization.events.addListener(chart, 'ready', function () {
    document.getElementById('png-questions').innerHTML = '<a href="' + chart.getImageURI() + '" download="questions_report">Download PNG</a>';
  });

  // Draw chart
  chart.draw(data, options)
}

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

window.onresize = function(){
  drawChartQuestions();
  drawChartStudentsiRAT();
  drawChartStudentsgRAT();
};

function parser(string) {
  var array = []
  var array1 = string.split("],")
  for (i in array1) {
    array1[i] = array1[i].replace(/\s/g, '')
    array1[i] = array1[i].replace(/'/g, '')
    array1[i] = array1[i].replace("[", '')
    array1[i] = array1[i].replace("[", '')
    array1[i] = array1[i].replace("]", '')
    array1[i] = array1[i].replace("]", '')
    var array2 = array1[i].split(",")
    array2[1] = parseInt(array2[1])
    array2[2] = parseInt(array2[2])
    array.push(array2)
  }
  return array
}