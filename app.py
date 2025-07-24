from flask import Flask
from dotenv import dotenv_values

app = Flask(__name__)

# load the configs from .env file as a dictionary
conf = dotenv_values('.env')

app.config["SECRET_KEY"] = conf["SECRET_KEY"] # Set < Secret Key > based on the environment

@app.route('/')
def home():
    return '<h1>Flask is born!</h1>'

if __name__ == '__main__':
    app.run()