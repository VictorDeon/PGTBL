google.charts.load('visualization', "1", {'packages': ['corechart']});

google.charts.setOnLoadCallback(drawChartQuestions);
google.charts.setOnLoadCallback(drawChartiRAT);
google.charts.setOnLoadCallback(drawChartgRAT);
google.charts.setOnLoadCallback(drawChartPeerReview);

function drawChartQuestions() {
    var data = new google.visualization.DataTable();
    var i;
    data.addColumn('string', 'Questões');
    data.addColumn('number', 'iRAT');
    data.addColumn('number', 'gRAT');

    data.addRows(RAT_count);

    for(i = 0; i < RAT_count; i++){
        data.setValue(i, 0, RAT_Questions[i]);
        data.setValue(i, 1, iRATTotalScore[i]);
        data.setValue(i, 2, gRATTotalScore[i]);
    }
    var options = {
        title: 'Quantidade de acertos por questões',
        hAxis: {title: 'Questões',  titleTextStyle: {color: '#333'}},
        vAxis: {title:'Quantidade de acertos', titleTextStyle: {color: '#333'}}
    }

    var chart = new google.visualization.AreaChart(document.getElementById('chart-questions'))

    google.visualization.events.addListener(chart, 'ready', function () {
        document.getElementById('png-questions').innerHTML = '<a href="' + chart.getImageURI() + '" download="questions_report">Download PNG</a>';
    });

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

function drawChartiRAT() {
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

function drawChartgRAT() {
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

    var options = {
        title: 'Pontuação por grupo: gRAT',
        legend: { position: 'none'},
        hAxis: {title: 'Pontuação',  minValue: 0, maxValue: 40, titleTextStyle: {color: '#333'}},
        vAxis: {title:'Grupos', titleTextStyle: {color: '#333'}},
        isStacked: true
    }


    var chart = new google.visualization.BarChart(document.getElementById('chart-students-grat'))

    google.visualization.events.addListener(chart, 'ready', function () {
        document.getElementById('png-grat').innerHTML = '<a href="' + chart.getImageURI() + '" download="gRAT_report">Download PNG</a>';
    });

    chart.draw(data, options)
}

function drawChartPeerReview() {
    var data = new google.visualization.DataTable();
    var i;

    data.addColumn('string', '');
    data.addColumn('number', 'Nota');

    data.addRows(student_count);

    for(i = 0; i < student_count; i++){
        data.setValue(i, 0, PeerReviewGrades[2*i]);
        data.setValue(i, 1, PeerReviewGrades[2*i+1]);
    }

    var options = {
        title: 'Pontuação por aluno: Peer Review',
        legend: {position: 'none'},
        hAxis: {title:'Alunos', titleTextStyle: {color: '#333'}},
        vAxis: {title: 'Pontuação',  minValue: 0, maxValue: 40, titleTextStyle: {color: '#333'}},
        isStacked: true
    }

    var chart = new google.visualization.ColumnChart(document.getElementById('chart-peerreview'))

    google.visualization.events.addListener(chart, 'ready', function () {
        document.getElementById('png-peer-review').innerHTML = '<a href="' + chart.getImageURI() + '" download="peer_review_report">Download PNG</a>';
    });

    chart.draw(data, options)
}

$(window).resize(function(){
  drawChartQuestions();
  drawChartiRAT();
  drawChartgRAT();
  drawChartPeerReview();
});
