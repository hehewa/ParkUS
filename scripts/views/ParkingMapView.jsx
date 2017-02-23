import React from 'react'
import {Map, Popup, Marker, TileLayer} from 'react-leaflet'
import L from 'Bower/leaflet/leaflet'

L.Icon.Default.imagePath = '/static/bower_components/leaflet/images';

class ParkingMap extends React.Component {
  constructor() {
    super();
  }
  renderMarkers() {
        return [...this.props.parkingSpots.values()].map((parkingSpot) =>
          parkingSpot.available? <Marker key={parkingSpot.position} position={parkingSpot.position} /> : null);
  }
  render() {
    return(
      <Map center={[51.505, -0.09]} zoom={18} className="parking-map" >
        <TileLayer
          url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
        />
        {this.renderMarkers()}
      </Map>
    );
  }
}

export default ParkingMap;
