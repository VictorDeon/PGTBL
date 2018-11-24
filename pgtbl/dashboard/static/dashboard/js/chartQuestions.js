// Callback that creates and populates a data table,
// instantiates the line chart, passes in the data and
// draws it.
function drawChartQuestions() {
  var graphic = document.getElementById('questions-data').innerHTML
  graphic = parser(graphic)
  graphic.splice(0, 0, ['Questões', 'iRAT', 'gRAT'])

  var optionsString = document.getElementById('questions-options').innerHTML
  optionsString = parserOptions(optionsString)

  // Create the table
  var data = new google.visualization.arrayToDataTable(graphic);

  // Set chart options
  var options = {
    title: optionsString[0],
    hAxis: {title: optionsString[1],  titleTextStyle: {color: '#333'}},
    vAxis: {title: optionsString[2], minValue: 0, maxValue: 50, titleTextStyle: {color: '#333'}}
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