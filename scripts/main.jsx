import ParkingMapApp from './containers/MapAppContainer'
import StatsApp from './containers/StatsAppContainer'
import React from 'react'
import ReactDOM from 'react-dom'

// suggéré par http://stackoverflow.com/questions/31933359/using-react-in-a-multi-page-app
const APPS = {
  ParkingMapApp,
  StatsApp,
}

function renderAppInElement(el) {
  var App = APPS[el.id];
  if(!App)
    return;

  ReactDOM.render(
    <App />,
    el
  );
}

for(var el of document.getElementsByClassName("main")) {
  renderAppInElement(el);
}
