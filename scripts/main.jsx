import AppContainer from './containers/AppContainer'
import React from 'react'
import ReactDOM from 'react-dom'

//TODO move this to its own file + support generic Action from ws payload?
import MapActions from './data/MapActions'
import io from 'socket.io-client'
var socket = io.connect('ws://' + document.domain + ':' + location.port);
socket.on('FULL_SYNC', (keyValuePairs) => {
  MapActions.fullSync(keyValuePairs)
});

ReactDOM.render(
  <AppContainer />,
  document.getElementById('main')
);
