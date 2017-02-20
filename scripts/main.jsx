import React from 'react'
import ReactDOM from 'react-dom'
import {Map, Popup, Marker, TileLayer} from 'react-leaflet'
import io from 'socket.io-client'
import L from 'Bower/leaflet/leaflet'

L.Icon.Default.imagePath = '/static/bower_components/leaflet/images';

var socket = io.connect('ws://' + document.domain + ':' + location.port);

class ParkingMap extends React.Component {
  constructor() {
    super();
    socket.on('full sync', this.onSync.bind(this));
    this.state = {
      mapCenter: [51.505, -0.09],
      destination: [51.505, -0.09],
      markers: []
    };
  }
  onSync(data) {
    this.setState({markers: data.parkings}); 
  }
  renderMarkers() {
        return this.state.markers.map((val, index) =>
          val.available? <Marker key={val.pos} position={val.pos} /> : null)
  }
  render() {
    return(
      <Map center={this.state.mapCenter} zoom={18} style={{width: '600px', height: '400px'}}>
        <TileLayer
          url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        {this.renderMarkers()}
      </Map>
    );
  }
}

class App extends React.Component {
  render() {
    return (
      <div className="app">
        <div className="map">
          <ParkingMap />
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <App />,
  document.getElementById('main')
);
