import React from 'react'
import GoogleChart from 'google-chart-react'

class AppView extends React.Component {
  constructor() {
    super();
    window.googleChartReactPackages = ['corechart'];
  }
  drawPieChart(chartID) {
    var data = new window.google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Slices');
    data.addRows([
      ['Mushrooms', 3],
      ['Onions', 1],
      ['Olives', 1],
      ['Zucchini', 1],
      ['Pepperoni', 2]
    ]);
    var options = {
      'title':'How Much Pizza I Ate Last Night',
      'width':400,
      'height':300
    };
    var chart = new window.google.visualization.PieChart(document.getElementById(chartID));
    chart.draw(data, options);
  }
  
  render() {
    return (<GoogleChart drawChart={this.drawPieChart} />);
  }
}

export default AppView;
