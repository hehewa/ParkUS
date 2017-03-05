#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_required, login_user, current_user
from user import User
from config import SECRET_KEY

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

socketio = SocketIO(app)

parkings = {
    '51.505,-0.09': {'position':[51.505, -0.09], 'reserved':False, 'available':True},
    '51.505,-0.09015': {'position':[51.505, -0.09015], 'reserved':False, 'available':True},
    '51.505,-0.0903': {'position':[51.505, -0.0903], 'reserved':False, 'available':False},
    '51.5048,-0.09': {'position':[51.5048, -0.09], 'reserved':False, 'available':False},
    '51.5048,-0.09015': {'position':[51.5048, -0.09015], 'reserved':False, 'available':True},
    '51.5048,-0.0903': {'position':[51.5048, -0.0903], 'reserved':False, 'available':False}
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

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
    parkings[key]['available'] = parkingSpot['available']
    emit('UPDATE', [[key, parkings[key]]], broadcast=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("login post")
        id = request.form['id']
        login_user(User(id))
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
