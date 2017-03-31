import MapActions from './data/MapActions'

var socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/wsmap');
socket.addEventListener('open', function (event) {
  socket.send('{"type":"connection"}');
});
socket.addEventListener('message', function (event) {
  var parsed = JSON.parse(event.data) 
  if(parsed["type"] == "FULL_SYNC") {
    MapActions.fullSync(parsed["args"]);
  } else if(parsed["type"] == "UPDATE") {
    MapActions.updateParkingSpots(parsed["args"]);
  }
});

/*Socket.on('FULL_SYNC', (keyValuePairs) => {
  MapActions.fullSync(keyValuePairs)
});

Socket.on('UPDATE', (keyValuePairs) => {
  MapActions.updateParkingSpots(keyValuePairs)
});*/

export default socket
