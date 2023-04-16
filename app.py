from random import random
from time import sleep
from threading import Thread, Event
import os

from flask import Flask, url_for, render_template, request, redirect, session, json, jsonify, copy_current_request_context
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
db = SQLAlchemy()
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

user_list = []

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    games_won = db.Column(db.Integer)
    games_played = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.games_won = 0
        self.games_played = 0

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String, unique=True) 
    player_1 = db.Column(db.Integer)
    player_2 = db.Column(db.Integer)
    player_3 = db.Column(db.Integer)
    player_4 = db.Column(db.Integer)
    player_5 = db.Column(db.Integer)
    player_6 = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='game',
                                lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    body = db.Column(db.String, unique=False) 
    emitted = db.Column(db.String, unique=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #try:
        db.session.add(User(username=request.form['username'], password=request.form['password']))
        db.session.commit()
        return redirect(url_for('login'))
        #except:
        #    return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            session['username'] = u
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/lobby', methods=['GET'])
#Once you are logged in, you are sent to lobby where you can join or create a game
def lobby():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/game/<game_id>', methods=['GET'])
#This will be the page that you get sent to after logging in
def game(game_id, methods = ['GET']):
    #users = db.session.query(User).all()
    if session.get('logged_in'):
        #return render_template('game.html')
        return render_template("game.html",users=user_list, game_id=game_id)
    else:
        return render_template('index.html', message="Hello!")


def gameManager():
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random()*10, 3)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(2)


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the game manager if it hasn't been started already
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(gameManager)

@socketio.on('join')
def join(message):
    join_room(message['room'])
    blnAlreadyInRoom = False
    for i in range(len(user_list)):
        if (user_list[i]['room'] == message['room'] and user_list[i]['username'] == session["username"]):
            blnAlreadyInRoom = True
            break
    if blnAlreadyInRoom == False:
        #Add the name to the game
        user_list.append({"username": session["username"], "room": message['room']})
    print(user_list)
    emit("join", {"username": session["username"], "room": message['room']}, broadcast=True)

@socketio.on("leave", namespace='/')
def left(message):
    #room = session["current_room"]
    print("leave")
    leave_room(message['room'])
    for i in range(len(user_list)):
        if (user_list[i]['room'] == message['room'] and user_list[i]['username'] == session["username"]):
            del user_list[i]
            break
    print(user_list)
    emit("leave", {"username": session["username"], "room": message['room']}, broadcast=True)

@socketio.on('new_message')
def handle_new_message(message):
    print(f"new message: {message}")
    print(session["username"])
    emit("chat", {"username": session["username"], "message": message}, broadcast=True)

@socketio.on('button')
def button_inputs(message):
    emit("chat", {"username": "Game", "message": message['button'] + " pressed by " + session["username"]}, broadcast=True)

app.secret_key = "ThisIsNotASecret:p"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.app_context().push()
db.init_app(app)
db.create_all()
db.session.commit()
socketio.run(app)