from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dotenv import dotenv_values

import db

app = Flask(__name__)

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


@ws.on('msg')
def message(data):
    print(f'{data} is received')
    db.save_msg(data)
    emit("messages", db.get_all_msg(), broadcast=True)

if __name__ == '__main__':
    ws.run(app, '0.0.0.0', debug=True)