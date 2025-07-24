from flask import Flask, render_template
from dotenv import dotenv_values

app = Flask(__name__)

# load the configs from .env file as a dictionary
conf = dotenv_values('.env')

app.config["SECRET_KEY"] = conf["SECRET_KEY"] # Set < Secret Key > based on the environment

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()