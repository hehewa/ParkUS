import MapActions from './data/MapActions'

var socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/wsmap');
socket.addEventListener('open', function (event) {
  socket.send('{"type":"connection"}');
});
socket.addEventListener('message', function (event) {
  var parsed = JSON.parse(event.data); 
  if(parsed["type"] == "FULL_SYNC") {
    MapActions.fullSync(parsed["args"]);
  } else if(parsed["type"] == "UPDATE") {
    MapActions.updateParkingSpots(parsed["args"]);
  } else if(parsed["type"] == "GATE") {
    if(window.location.pathname == "/login") {
      if(parsed["args"]["success"]) {
        console.log("success : " + parsed["args"]["id"]);
        var form = $(".login-form");
        var inputField = $(".login-id");
        inputField.val(parsed["args"]["id"].toString());
        form.submit();
      } else {
        console.log("fail : " + parsed["args"]["id"]);
        var message = $(".login-error");
        message.css("display", "block");
      }
    }
  }
});

export default socket
