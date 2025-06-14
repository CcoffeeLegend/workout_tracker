from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

USERDATA_FILE = "userdata.json"

def load_userdata():
    if os.path.exists(USERDATA_FILE):
        with open(USERDATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_userdata(data):
    with open(USERDATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"].strip().lower()
    password = data["password"]
    userdata = load_userdata()
    if username in userdata:
        return jsonify({"error": "Username already exists"}), 400
    userdata[username] = {"password": password, "routine": []}
    save_userdata(userdata)
    return jsonify({"message": "Registered successfully"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"].strip().lower()
    password = data["password"]
    userdata = load_userdata()
    if username in userdata and userdata[username]["password"] == password:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/routine/<username>", methods=["GET", "POST"])
def routine(username):
    userdata = load_userdata()
    if username not in userdata:
        return jsonify({"error": "User not found"}), 404
    if request.method == "GET":
        return jsonify(userdata[username]["routine"])
    elif request.method == "POST":
        exercise = request.json
        userdata[username]["routine"].append(exercise)
        save_userdata(userdata)
        return jsonify({"message": "Exercise added"})

if __name__ == "__main__":
    app.run(debug=True)