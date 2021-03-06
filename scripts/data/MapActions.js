import MapActionTypes from './MapActionTypes'
import MapDispatcher from './MapDispatcher'
import socket from '../websocket'

const Actions = {
  fullSync(keyValuePairs) {
    MapDispatcher.dispatch({
      type: MapActionTypes.FULL_SYNC,
      keyValuePairs,
    });
  },
  updateParkingSpots(keyValuePairs) {
    MapDispatcher.dispatch({
      type: MapActionTypes.UPDATE_PARKING_SPOTS,
      keyValuePairs,
    });
  },
  onReservation(key, reserved) {
    socket.send(JSON.stringify({type:'RESERVATION', args:{key: key, reserved: reserved}}));
    document.location = '/logout';
  },
  onParkingSpotUpdate(position, available) {
    Socket.emit('FAKE_UPDATE', {position: position, available: available, reserved: false});
  }
};

export default Actions;
