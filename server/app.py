#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, g
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_required, login_user, current_user
from user import User
from utils import admin_only, authenticated_only
from config import SECRET_KEY

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

socketio = SocketIO(app)

parkings = {
    '51.50512,-0.0901': {'position':[51.50512, -0.0901], 'reserved':False, 'available':True},
    '51.50503,-0.0901': {'position':[51.50503, -0.0901], 'reserved':False, 'available':True},
    '51.50494,-0.0901': {'position':[51.50494, -0.0901], 'reserved':False, 'available':False},
    '51.50485,-0.0901': {'position':[51.50485, -0.0901], 'reserved':False, 'available':False},
    '51.50476,-0.0901': {'position':[51.50476, -0.0901], 'reserved':False, 'available':True},
    '51.50467,-0.0901': {'position':[51.50467, -0.0901], 'reserved':False, 'available':False}
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@socketio.on('connect')
@authenticated_only
def on_connect():
    # il est attendu que le client resynchronise
    # l'entierté des places
    emit('FULL_SYNC', list(parkings.items()))

@socketio.on('RESERVATION')
@authenticated_only
def on_reservation(parkingSpot):
    key = ','.join(map(str,parkingSpot['position']))
    if parkings[key]['reserved'] != parkingSpot['reserved']:
        parkings[key]['reserved'] = parkingSpot['reserved']
        emit('UPDATE', [[key, parkings[key]]], broadcast=True)

@socketio.on('FAKE_UPDATE')
@authenticated_only
def on_fake_update(parkingSpot):
    # test update provenant du UI
    # a remplacer par message du microcontrôleur coordo
    key = ','.join(map(str,parkingSpot['position']))
    parkings[key]['available'] = parkingSpot['available']
    emit('UPDATE', [[key, parkings[key]]], broadcast=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        login_user(User(user_id))
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@app.route('/stats')
@admin_only
def stats():
    return render_template('stats.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_id = request.form['email']
        login_user(User(1))
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

if __name__ == '__main__':
    socketio.run(app, debug=True)
