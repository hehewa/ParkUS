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
      if(!parsed["args"]["success"]) {
        console.log("fail : " + parsed["args"]["id"]);
        var messageBox = $(".login-error");
        var message = $(".login-message");
        message.html("Carte non reconnue. <a href='/signup'>Abonnez-vous!</a>");
        messageBox.css("display", "block");
      } else if(parsed["args"]["full"]) {
        console.log("fail : " + parsed["args"]["id"]);
        var messageBox = $(".login-error");
        var message = $(".login-message");
        message.html("Stationnement &agrave; pleine capacit&eacute;.");
        messageBox.css("display", "block");
      } else if(parsed["args"]["success"]) {
        console.log("success : " + parsed["args"]["id"]);
        var form = $(".login-form");
        var inputField = $(".login-id");
        inputField.val(parsed["args"]["id"].toString());
        form.submit();
      }
    }
  }
});

export default socket
