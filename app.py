from flask import Flask, url_for, redirect, render_template, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS


import random

app = Flask(__name__, template_folder='templates')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/')
def index():

    room = db.session.query(Room.name).order_by(func.random()).first()
    character = db.session.query(Character.name).order_by(func.random()).first()
    weapon = db.session.query(Weapon.name).order_by(func.random()).first()

    print("Query: ", room.name)
    test = "It was " + str(character.name) + " in the " + str(room.name) + " with the " + str(weapon.name) + "!"
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        solution = {'room': room.name, 'character': character.name, 'weapon': weapon.name }
        return jsonify(solution)

    return render_template("home.html",room=room.name, character=character.name, weapon=weapon.name)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')