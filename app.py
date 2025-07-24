from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dotenv import dotenv_values

app = Flask(__name__)

# load the configs from .env file as a dictionary
conf = dotenv_values('.env')
app.config["SECRET_KEY"] = conf["SECRET_KEY"] # Set < Secret Key > based on the environment

ws = SocketIO(app)


@app.route('/')
def home():
    return render_template("index.html")


@ws.on('test')
def test(data):
    print(f'{data} is received')
    emit("msg", f"{data} is received")

if __name__ == '__main__':
    ws.run(app, debug=True)