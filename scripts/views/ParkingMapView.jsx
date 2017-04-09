import React from 'react'
import {Map, Popup, Marker, ImageOverlay} from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'Css/leaflet-style.css'
import 'leaflet/dist/images/marker-icon.png'
import 'leaflet/dist/images/marker-icon-2x.png'
import 'leaflet/dist/images/marker-shadow.png'
import L from 'leaflet'

L.Icon.Default.imagePath = '/static/img/';

var reservedIcon = new L.Icon.Default();
reservedIcon.options.iconUrl = 'marker-orange.png';
var availableIcon = new L.Icon.Default()

var b = [[51.5045, -0.089], [51.5055, -0.091]]

class ParkingMap extends React.Component {
  constructor() {
    super();
  }
  renderPopup(key, parkingSpot) {
    return (<Popup>
              <button
                type="button" className="btn btn-success btn-popup"
                onClick={() => this.props.onReservation(key, !parkingSpot.reserved)}>
                {
                  parkingSpot.reserved?
                    "Annuler la réservation" :
                    "Confirmer la réservation"
                }
              </button>
            </Popup>);
  }
  renderMarkers() {
    return [...this.props.parkingSpots.entries()].map((entry) =>
      entry[1].available? (<Marker
                                key={entry[0]}
                                position={entry[1].position}
                                icon={entry[1].reserved? reservedIcon : availableIcon}>
                                {this.renderPopup(...entry)}
                              </Marker>) : null);
  }
  render() {
    return(
      <Map center={[51.505, -0.09]} zoom={19} className="parking-map" maxBounds={b}>
        <ImageOverlay
          url='/static/img/parking-map-test.png'
          bounds={b}
        />
        {this.renderMarkers()}
      </Map>
    );
  }
}

export default ParkingMap;
