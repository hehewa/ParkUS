import {ReduceStore} from 'flux/utils'
import MapActionTypes from './MapActionTypes'
import MapDispatcher from './MapDispatcher'

class MapStore extends ReduceStore {
  constructor() {
    super(MapDispatcher);
  }

  getInitialState() {
    return new Map();
  }

  reduce(state, action) {
    switch (action.type) {
      case MapActionTypes.FULL_SYNC:
        return new Map(action.keyValuePairs);

      case MapActionTypes.UPDATE_PARKING_SPOTS:
        return new Map([...state, ...action.keyValuePairs]);

      default:
        return state;
    }
  }
}

export default new MapStore();
