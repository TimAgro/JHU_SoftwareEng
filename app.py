#from flask import Flask, url_for, redirect, render_template, request, json, jsonify, session
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import func
#from flask_cors import CORS



from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

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
def game(game_id):
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")

app.secret_key = "ThisIsNotASecret:p"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.app_context().push()
db.init_app(app)
db.create_all()
db.session.commit()



'''
app = Flask(__name__, template_folder='templates')
db = SQLAlchemy()

# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

app.secret_key = "ThisIsNotASecret:p"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.app_context().push()
db.init_app(app)
db.create_all()
db.session.commit()

@app.route('/')
def index():

    room = db.session.query(Room.name).order_by(func.random()).first()
    character = db.session.query(Character.name).order_by(func.random()).first()
    weapon = db.session.query(Weapon.name).order_by(func.random()).first()

    #print("Query: ", room.name)
    #test = "It was " + str(character.name) + " in the " + str(room.name) + " with the " + str(weapon.name) + "!"
    
    #if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #    solution = {'room': room.name, 'character': character.name, 'weapon': weapon.name }
    #    return jsonify(solution)

    #return render_template("home.html",room=room.name, character=character.name, weapon=weapon.name)
    return "test"

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

'''
