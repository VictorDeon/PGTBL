google.charts.load('visualization', "1", {'packages': ['corechart']});

google.charts.setOnLoadCallback(drawChartQuestions);
google.charts.setOnLoadCallback(drawChartStudentsiRAT);
google.charts.setOnLoadCallback(drawChartStudentsgRAT);

function drawChartQuestions() {
  // Create the table
  var data = new google.visualization.arrayToDataTable([
    ['Questões', 'iRAT', 'gRAT'],
    ['Q1',  10, 20],
    ['Q2',  25, 33],
    ['Q3',  8,   15],
    ['Q4',  32, 50],
    ['Q5',  40, 50],
    ['Q6',  50, 50],
    ['Q7',  22, 32],
    ['Q8',  11, 10],
    ['Q9',  27, 20],
    ['Q10', 10, 20],
  ]);

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

function gradeColor(grade){
  if (grade < 1) {
    return 'rgb(200, 0, 0)';
  } else if (grade < 4) {
   return 'rgb(255, 204, 0)';
  } else {
    return 'rgb(0, 153, 0)';
  }
}

function drawChartStudentsiRAT() {
  var data = new google.visualization.DataTable();
      var i;
      var j;
      var column = 0;
      var bar_size = 5;
      var str;

      data.addColumn('string', '');
      for(i = 0; i < RAT_count; i++){
          data.addColumn('number', RAT_Questions[i]);
          data.addColumn({ type: 'string', role: 'style' });
          data.addColumn({ type: 'string', role: 'tooltip' });
      }

  data.addRows(student_count);

      for(i = 0; i < student_count; i++){
          column = 0;
          data.setValue(i, column++, student_list[i]);

          for(j = 0; j < iRATSubmissions_count; j++){
              if (iRATSubmissions[3*j] == student_list[i]){
                  grade = iRATSubmissions[3*j+2];

                  data.setValue(i, column++, bar_size);
                  data.setValue(i, column++, gradeColor(grade));

                  str = iRATSubmissions[3*j+1].concat('\nPontuação: ');
                  data.setValue(i, column++, str.concat(grade.toString()));
              }
          }
      }

  var options = {
    title: 'Pontuação por aluno: iRAT',
    legend: {position: 'none'},
    hAxis: {title: 'Pontuação',  minValue: 0, maxValue: 40, titleTextStyle: {color: '#333'}},
    vAxis: {title:'Alunos', titleTextStyle: {color: '#333'}},
    isStacked: true
  }

  var chart = new google.visualization.BarChart(document.getElementById('chart-students-irat'))

  google.visualization.events.addListener(chart, 'ready', function () {
    document.getElementById('png-irat').innerHTML = '<a href="' + chart.getImageURI() + '" download="iRAT_report">Download PNG</a>';
  });

  chart.draw(data, options)
}

function drawChartStudentsgRAT() {
    var data = new google.visualization.DataTable();
    var i;
    var j;
    var column = 0;
    var bar_size = 5;
    var str;

    data.addColumn('string', '');
    for(i = 0; i < RAT_count; i++){
        data.addColumn('number', RAT_Questions[i]);
        data.addColumn({ type: 'string', role: 'style' });
        data.addColumn({ type: 'string', role: 'tooltip' });
    }

    data.addRows(groups_count);

    for(i = 0; i < groups_count; i++){
        column = 0;
        data.setValue(i, column++, groups[i]);

        for(j = 0; j < gRATSubmissions_count; j++){
            if (gRATSubmissions[3*j] == groups[i]){
                grade = gRATSubmissions[3*j+2];

                data.setValue(i, column++, bar_size);
                data.setValue(i, column++, gradeColor(grade));

                str = gRATSubmissions[3*j+1].concat('\nPontuação: ');
                data.setValue(i, column++, str.concat(grade.toString()));
            }
        }
    }

  // Set chart options
  var options = {
    title: 'Pontuação por grupo: gRAT',
    legend: { position: 'none'},
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

$(window).resize(function(){
  drawChartQuestions();
  drawChartStudentsiRAT();
  drawChartStudentsgRAT();
});
