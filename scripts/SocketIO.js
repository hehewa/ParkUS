import MapActions from './data/MapActions'
import io from 'socket.io-client'

var Socket = io.connect('ws://' + document.domain + ':' + location.port);
Socket.on('FULL_SYNC', (keyValuePairs) => {
  MapActions.fullSync(keyValuePairs)
});

Socket.on('UPDATE', (keyValuePairs) => {
  MapActions.updateParkingSpots(keyValuePairs)
});

export default Socket
