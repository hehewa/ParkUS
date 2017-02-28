#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, static_folder='../static', template_folder='../templates')
socketio = SocketIO(app)

parkings = {
    '51.505,-0.09': {'position':[51.505, -0.09], 'reserved':False, 'available':True},
    '51.505,-0.09015': {'position':[51.505, -0.09015], 'reserved':False, 'available':True},
    '51.505,-0.0903': {'position':[51.505, -0.0903], 'reserved':False, 'available':False},
    '51.5048,-0.09': {'position':[51.5048, -0.09], 'reserved':False, 'available':False},
    '51.5048,-0.09015': {'position':[51.5048, -0.09015], 'reserved':False, 'available':True},
    '51.5048,-0.0903': {'position':[51.5048, -0.0903], 'reserved':False, 'available':False}
}

@socketio.on('connect')
def on_connect():
    # il est attendu que le client resynchronise
    # l'entierté des places
    emit('FULL_SYNC', list(parkings.items()))

@socketio.on('RESERVATION')
def on_reservation(parkingSpot):
    key = ','.join(map(str,parkingSpot['position']))
    if parkings[key]['reserved'] != parkingSpot['reserved']:
        parkings[key]['reserved'] = parkingSpot['reserved']
        emit('UPDATE', [[key, parkings[key]]], broadcast=True)

@socketio.on('FAKE_UPDATE')
def on_fake_update(parkingSpot):
    # test update provenant du UI
    # a remplacer par message du microcontrôleur coordo
    key = ','.join(map(str,parkingSpot['position']))
    parkings[key] = parkingSpot
    emit('UPDATE', [[key, parkingSpot]], broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
