import AppView from '../views/AppView.jsx'
import {Container} from 'flux/utils'
import MapStore from '../data/MapStore'

function getStores() {
  return [
    MapStore,
  ];
}

function getState() {
  return {
    parkingSpots: MapStore.getState(),
  };
}

export default Container.createFunctional(AppView, getStores, getState);
