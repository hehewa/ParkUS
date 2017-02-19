#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

parkings = {'parkings':[ 
    {'pos':[51.505, -0.09], 'available':True},
    {'pos':[51.505, -0.09015], 'available':False},
    {'pos':[51.505, -0.0903], 'available':True},
    {'pos':[51.5048, -0.09], 'available':False},
    {'pos':[51.5048, -0.09015], 'available':False},
    {'pos':[51.5048, -0.0903], 'available':True}
]}

@socketio.on('connect')
def on_connect():
    # il est attendu que le client resynchronise
    # l'entierté des places
    emit('full sync', parkings)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
