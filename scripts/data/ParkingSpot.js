import Immutable from 'immutable'

const ParkingSpot = Immutable.Record({
  position: [],
  available: false,
  reserved: false
});

export default ParkingSpot;
