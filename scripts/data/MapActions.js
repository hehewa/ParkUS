import MapActionTypes from './MapActionTypes'
import MapDispatcher from './MapDispatcher'

const Actions = {
  fullSync(keyValuePairs) {
    MapDispatcher.dispatch({
      type: MapActionTypes.FULL_SYNC,
      keyValuePairs,
    });
  }
};

export default Actions;
