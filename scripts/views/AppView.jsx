import React from 'react'
import ParkingMap from './ParkingMapView.jsx'
import TestInput from './TestInputView.jsx'

function AppView(props) {
  return (
    <div className="app">
      <div className="map">
        <ParkingMap {...props} />
        <TestInput {...props} />
      </div>
    </div>
  );
}

export default AppView;
