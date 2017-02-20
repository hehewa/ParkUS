import AppView from '../views/AppView.jsx'
import {Container} from 'flux/utils'
import MapStore from '../data/MapStore'
import MapActions from '../data/MapActions'

function getStores() {
  return [
    MapStore,
  ];
}

function getState() {
  return {
    parkingSpots: MapStore.getState(),
    onParkingSpotUpdate: MapActions.onParkingSpotUpdate
  };
}

export default Container.createFunctional(AppView, getStores, getState);
