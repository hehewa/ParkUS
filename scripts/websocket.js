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
  } else if(parsed["type"] == "GATE") {
    if(parsed["args"]["success"]) {
      console.log("success : " + parsed["args"]["id"])
    } else {
      console.log("fail : " + parsed["args"]["id"])
    }
  }
});

export default socket
