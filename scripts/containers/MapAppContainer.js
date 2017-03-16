import AppView from '../views/MapAppView.jsx'
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
    onParkingSpotUpdate: MapActions.onParkingSpotUpdate,
    onReservation: MapActions.onReservation
  };
}

export default Container.createFunctional(AppView, getStores, getState);
