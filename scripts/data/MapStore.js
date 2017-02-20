import Immutable from 'immutable'
import {ReduceStore} from 'flux/utils'
import MapActionTypes from './MapActionTypes'
import MapDispatcher from './MapDispatcher'
import ParkingSpot from '../data/ParkingSpot'

class MapStore extends ReduceStore {
  constructor() {
    super(MapDispatcher);
  }

  getInitialState() {
    return Immutable.Map();
  }

  reduce(state, action) {
    switch (action.type) {
      case MapActionTypes.FULL_SYNC:
        return Immutable.Map(action.keyValuePairs);

      default:
        return state;
    }
  }
}

export default new MapStore();
