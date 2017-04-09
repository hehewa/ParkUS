import React from 'react'
import ParkingMap from './ParkingMapView.jsx'
import TestInput from './TestInputView.jsx'

function AppView(props) {
  return (
    <div>
      <ParkingMap {...props} />
      {/*<TestInput {...props} />*/}
    </div>
  );
}

export default AppView;
