from random import random
from time import sleep
from threading import Thread, Event
import os

from flask import Flask, url_for, render_template, request, redirect, session, json, jsonify, copy_current_request_context
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import game

app = Flask(__name__)
db = SQLAlchemy()
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

user_list = []
games = []

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


@app.route('/game/<game_id>', methods=['GET'])
#This will be the page that you get sent to after logging in
def gameroute(game_id, methods = ['GET']):
    #users = db.session.query(User).all()
    if session.get('logged_in'):
        #return render_template('game.html')
        return render_template("game.html",users=user_list, game_id=game_id,player_id=session["username"])
    else:
        return render_template('index.html', message="Hello!")


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')


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
    #Do something. Check game engine
    emit("chat", {"username": "Game", "message": message['button'] + " pressed by " + session["username"]}, broadcast=True)

@socketio.on('restart')
def restart(message):
    
    #Should find and replace the correct game
    #games = []

    ######figure out which players are in the game
    ##ONLY register real player_ids
    print(user_list)
    user_array = []
    for i in range(len(user_list)):
        if (user_list[i]['room'] == message['game_id']):
            user_array.append(user_list[i]['username'])

    #add players from the room into the game manager.
    gm = game.GameManager(user_array,message['game_id'])
    games.append(gm)

    player_grid = []
    for i, list in enumerate(gm.gb.player_grid):
        for j, item in enumerate(list):
            if item != 0:
                player_grid.append({"type":item, "x": i, "y": j})
    player_dict = {item['type']:item for item in player_grid}

    deck_list = []
    for i, list in enumerate(gm.deck.hands):
        for j, item in enumerate(list):
            if item != 0:
                deck_list.append({"card":item, "hand": i})
    deck_dict = {item['card']:item for item in deck_list}

    #Do the same for players
    players_dict = {item['player_ID']:item for item in gm.players}
    print(players_dict)

    emit("restart", {"player_grid": player_dict, "deck": deck_dict, "players_dict": players_dict, "turn_count": gm.turn_count}, broadcast=True)


@socketio.on('move')
def move(message):
    #Get the game_ID
    game_ID = message['game_id']
    player_id = message['player_id']
    
    #print(games) 
    #for this_game in games:
    #    print(this_game)
    #    print(this_game.game_ID)
    #    if this_game.game_ID == game_ID:
    #        gm =this_game.game_ID
    #        break
    gm = games[0]

    print(game_ID,player_id, message['direction'])

    move_result = gm.move(player_id, message['direction'])
    players_dict = {item['player_ID']:item for item in gm.players}
    
    emit("move",{"player_id": player_id, "move_result": move_result, "players_dict": players_dict,"turn_count": gm.turn_count}, broadcast=True)


@socketio.on('suggestion')
def suggestion(message):
    #Get the game_ID
    game_ID = message['game_id']
    player_id = message['player_id']

    print(games) 
    for this_game in games:
        print(this_game)
        print(this_game.game_ID)
        if this_game.game_ID == game_ID:
            gm =this_game.game_ID
            break

    #suggestion_result = gm.check_suggestion(player_id, message['card1'], message['card2'], message['card3'])
    suggestion_result = True
    emit("suggestion",{"player_id": player_id, "suggestion_result": suggestion_result}, broadcast=True)


@socketio.on('accusation')
def accusation(message):
    #Get the game_ID
    game_ID = message['game_id']
    player_id = message['player_id']
     
    for this_game in games:
        if this_game.game_ID == game_ID:
            gm =this_game.game_ID
            break

    accusation_result = gm.check_accusation(player_id, message['card1'], message['card2'], message['card3'])
    emit("accusation",{"player_id": player_id, "accusation_result": accusation_result}, broadcast=True)


@socketio.on('turn_check')
def turn_check(message):
    #Get the game_ID
    game_id = message['game_id']
    player_id = message['player_id']
     
    for this_game in games:
        if this_game.game_id == game_id:
            gm =this_game.game_id
            break

    turn_check = gm.check_turn(player_id)
    emit("accusation",{"player_id": player_id, "turn_check_result": turn_check}, broadcast=True)


app.secret_key = "ThisIsNotASecret:p"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.app_context().push()
db.init_app(app)
db.create_all()
db.session.commit()


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5004)