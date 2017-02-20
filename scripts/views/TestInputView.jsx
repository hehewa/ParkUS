import React from 'react'

function TestInput(props) {
  return (
    <div>
      {[...props.parkingSpots.values()].map((parkingSpot) =>
        <input key={parkingSpot.position} type="checkbox" checked={parkingSpot.available} onChange={() => props.onParkingSpotUpdate(parkingSpot.position,!parkingSpot.available)} />)}
    </div>
  );
}

export default TestInput;
