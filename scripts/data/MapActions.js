import MapActionTypes from './MapActionTypes'
import MapDispatcher from './MapDispatcher'
import Socket from '../SocketIO'

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
  onReservation(position, reserved) {
    Socket.emit('RESERVATION', {position: position, reserved: reserved});
  },
  onParkingSpotUpdate(position, available) {
    Socket.emit('FAKE_UPDATE', {position: position, available: available, reserved: false});
  }
};

export default Actions;
