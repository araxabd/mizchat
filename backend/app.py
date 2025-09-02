from datetime import datetime, timedelta
from flask import Flask, request, make_response, jsonify
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import dotenv_values
import jwt
import sqlite3

import db

app = Flask(__name__)

# Initialize bcrypt for hashing passwords
bcrypt = Bcrypt(app)

# load the configs from .env file as a dictionary
conf = dotenv_values('.env')

# Set app configurations
app.config["SECRET_KEY"] = conf["SECRET_KEY"] # Set < Secret Key > based on the environment
# CORS Configurations
app.config["CORS_SUPPORTS_CREDENTIALS"] = True
CORS(app, supports_credentials=True, origins=["http://localhost:8000", "http://192.168.1.81:5000"])

# Start WebSocket
ws = SocketIO(app, cors_allowed_origins="*")

# Initialize database
db.init()

# Temporary
@app.route('/getusername')
def get_username():
    tk = request.cookies.get("token")
    if not tk:
        return jsonify({"err": "Unauthorized"}), 401
    try:
        pl = jwt.decode(tk, app.config["SECRET_KEY"], algorithms=["HS256"])
        user = db.get_user_by_id(pl["user_id"])
        return jsonify({"username": user[1]})
    except jwt.ExpiredSignatureError:
        return jsonify({"err": "Token expired"})
    except jwt.InvalidTokenError:
        return jsonify({"err": "Token is invalid"})




def generate_token(user_id):
    return jwt.encode(
        {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user = db.get_user_by_username(data["username"])
    if user and bcrypt.check_password_hash(user[2], data["password"]):
        tk = generate_token(user[0])
        res = make_response(jsonify({"success": True}))
        res.set_cookie(
            "token",
            value=tk,
            httponly=True,
            # secure=True,  Uncomment it for deployment
            samesite="LAX",
            max_age=3600
        )
        return res
    return jsonify({"success": False}), 401


@app.route('/logout', methods=["POST"])
def logout():
    res = make_response(jsonify({"success": True}))
    res.delete_cookie("token")
    return res


@app.route('/signup', methods=["POST"])
def signup():
    user = request.get_json()
    hashed_password = bcrypt.generate_password_hash(user["password"]).decode("utf-8")
    print(user["username"], hashed_password)
    try:
        db.set_user(user["username"], hashed_password)
        print("user is set")
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "err": "Username is taken"}), 400


@app.route('/is-authenticated', methods=["GET"])
def auth_verification():
    tk = request.cookies.get("token")
    if not tk:
        return jsonify({"authenticated": False, "err": "No token"}), 401
    
    try:
        pl = jwt.decode(tk, app.config["SECRET_KEY"], algorithms=["HS256"])
        return jsonify({"authenticated": True, "user_id": pl["user_id"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"authenticated": False, "err": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"authenticated": False, "err": "Invalid token"}), 401

# @ws.on('msg')
# def message(data):
#     print(f'{data} is received')
#     db.save_msg(data)
#     emit("messages", db.get_all_msg(), broadcast=True)


if __name__ == '__main__':
    ws.run(app, '0.0.0.0', debug=True)
