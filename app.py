#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

parkings = [
    [[51.505, -0.09], {'position':[51.505, -0.09], 'reserved':False, 'available':True}],
    [[51.505, -0.09015], {'position':[51.505, -0.09015], 'reserved':False, 'available':True}],
    [[51.505, -0.0903], {'position':[51.505, -0.0903], 'reserved':False, 'available':False}],
    [[51.5048, -0.09], {'position':[51.5048, -0.09], 'reserved':False, 'available':False}],
    [[51.5048, -0.09015], {'position':[51.5048, -0.09015], 'reserved':False, 'available':True}],
    [[51.5048, -0.0903], {'position':[51.5048, -0.0903], 'reserved':False, 'available':False}]
]

@socketio.on('connect')
def on_connect():
    # il est attendu que le client resynchronise
    # l'entierté des places
    emit('FULL_SYNC', parkings)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
