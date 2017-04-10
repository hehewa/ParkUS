import React from 'react'
import GoogleChart from 'google-chart-react'

class AppView extends React.Component {
  constructor() {
    super();
    window.googleChartReactPackages = ['corechart'];
  }
  drawBarChart(chartID) {
    var data = google.visualization.arrayToDataTable([
      ['Heure', "Taux d'occupation", "Taux d'occupation moyen"],
      ['04 h', 5, 10],
      ['05 h', 8, 20],
      ['06 h', 8, 30],
      ['07 h', 30, 40],
      ['08 h', 50, 50],
      ['09 h', 80, 70],
      ['10 h', 80, 70],
      ['11 h', 80, 91],
      ['12 h', 80, 60],
      ['13 h', 90, 60],
      ['14 h', 90, 60],
      ['15 h', 70, 70],
      ['16 h', 70, 70],
      ['17 h', 60, 50],
      ['18 h', 60, 40],
      ['19 h', 60, 20],
      ['20 h', 60, 10],
      ['21 h', 50, 5]
    ]);
    var options = {
      title: "Taux d'occupation horaire",
      colors: ['#b0120a', '#ffab91'],
      hAxis: {
        title: "Taux d'occupation",
        minValue: 0,
        maxValue: 100
      },
      vAxis: {
        title: 'Heure'
      },
      width: 900,
      height: 500
    };
    var chart = new google.visualization.BarChart(document.getElementById(chartID));
    chart.draw(data, options);
  }
  drawPieChart(chartID) {
    var data = new window.google.visualization.DataTable();
    data.addColumn('string', 'Type');
    data.addColumn('number', 'Compte');
    data.addRows([
      ['Journalier', 5],
      ['Annuel', 12],
      ['Mensuel', 2]
    ]);
    var options = {
      'title':"Type d'abonnement",
      'width': 400,
      'height': 300
    };
    var chart = new window.google.visualization.PieChart(document.getElementById(chartID));
    chart.draw(data, options);
  }
  
  render() {
    return (
      <span>
        <GoogleChart drawChart={this.drawBarChart} />
        <br/>
        <GoogleChart drawChart={this.drawPieChart} />
      </span>
    );
  }
}

export default AppView;
