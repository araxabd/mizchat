from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dotenv import dotenv_values

from db import init, save_msg, get_all_msg

app = Flask(__name__)

# load the configs from .env file as a dictionary
conf = dotenv_values('.env')
app.config["SECRET_KEY"] = conf["SECRET_KEY"] # Set < Secret Key > based on the environment

# Start WebSocket
ws = SocketIO(app)

# Initialize database
init()


@app.route('/')
def home():
    return render_template("index.html")


@ws.on('msg')
def message(data):
    print(f'{data} is received')
    save_msg(data)
    emit("messages", get_all_msg())

if __name__ == '__main__':
    ws.run(app, debug=True)