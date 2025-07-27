from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from dotenv import dotenv_values

import db

app = Flask(__name__)

# Initialize bcrypt for hashing passwords
bcrypt = Bcrypt(app)

# load the configs from .env file as a dictionary
conf = dotenv_values('.env')
app.config["SECRET_KEY"] = conf["SECRET_KEY"] # Set < Secret Key > based on the environment

# Start WebSocket
ws = SocketIO(app, cors_allowed_origins="*")

# Initialize database
db.init()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.get_user(username)
        correct_hashed_pass = user[1]
        if bcrypt.check_password_hash(correct_hashed_pass, password):
            #TODO: handle login with flask-login and create a get_user_by_id function in db



@ws.on('msg')
def message(data):
    print(f'{data} is received')
    db.save_msg(data)
    emit("messages", db.get_all_msg(), broadcast=True)


if __name__ == '__main__':
    ws.run(app, '0.0.0.0', debug=True)