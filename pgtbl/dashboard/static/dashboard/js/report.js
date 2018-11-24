// Load the Visualization API and the corechart package.
google.charts.load('visualization', "1", {'packages': ['corechart']});
// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChartQuestions);
google.charts.setOnLoadCallback(drawChartStudentsiRAT);
google.charts.setOnLoadCallback(drawChartStudentsgRAT);

window.onresize = function(){
  drawChartQuestions();
  drawChartStudentsiRAT();
  drawChartStudentsgRAT();
};