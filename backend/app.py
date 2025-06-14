from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Use SQLite for local development; switch to PostgreSQL for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    routines = db.relationship('Routine', backref='user', lazy=True)
    unit = db.Column(db.String(2), default="lb")  # "lb" or "kg"
    goal = db.Column(db.String(32), default="bodybuilding")  # or "powerlifting"

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(120), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weights = db.Column(db.String(120), nullable=False)  # Store as comma-separated string
    auto_increment = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400
    username = data["username"].strip().lower()
    password = data["password"]
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    user = User()
    user.username = username
    user.password = password
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"})

# ...existing code...

# Removed duplicate get_routine route handler to avoid function name conflict.


@app.route("/api/routine/<username>/<int:rid>", methods=["PUT"])
def update_routine(username, rid):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    routine = Routine.query.filter_by(id=rid, user_id=user.id).first()
    if not routine:
        return jsonify({"error": "Routine not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    routine.exercise = data.get("exercise", routine.exercise)
    routine.sets = data.get("sets", routine.sets)
    routine.reps = data.get("reps", routine.reps)
    if "weights" in data:
        routine.weights = ','.join(str(w) for w in data["weights"])
    routine.auto_increment = data.get("auto_increment", routine.auto_increment)
    db.session.commit()
    return jsonify({"message": "Exercise updated"})

@app.route("/api/routine/<username>/<int:rid>", methods=["DELETE"])
def delete_routine_v1(username, rid):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    routine = Routine.query.filter_by(id=rid, user_id=user.id).first()
    if not routine:
        return jsonify({"error": "Routine not found"}), 404
    db.session.delete(routine)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400
    username = data["username"].strip().lower()
    password = data["password"]
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/routine/<username>", methods=["GET", "POST"])
def routine(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if request.method == "GET":
        routines = [
            {
                "exercise": r.exercise,
                "sets": r.sets,
                "reps": r.reps,
                "weights": [int(w) for w in r.weights.split(',')],
                "auto_increment": r.auto_increment
            }
            for r in user.routines
        ]
        return jsonify(routines)
    elif request.method == "POST":
        data = request.json
        required_fields = ["exercise", "sets", "reps", "weights", "auto_increment"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required routine fields"}), 400
        routine = Routine()
        routine.exercise = data["exercise"]
        routine.sets = data["sets"]
        routine.reps = data["reps"]
        routine.weights = ','.join(str(w) for w in data["weights"])
        routine.auto_increment = data["auto_increment"]
        routine.user_id = user.id
        db.session.add(routine)
        db.session.commit()
        return jsonify({"message": "Exercise added"})
    return jsonify({"error": "Method not allowed"}), 405

# ...existing code...

@app.route("/api/routine/<username>", methods=["GET"])
def get_routine(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    routines = [
        {
            "id": r.id,
            "exercise": r.exercise,
            "sets": r.sets,
            "reps": r.reps,
            "weights": [int(w) for w in r.weights.split(',')],
            "auto_increment": r.auto_increment
        }
        for r in user.routines
    ]
    return jsonify(routines)

@app.route("/api/routine/<username>", methods=["POST"])
def add_routine(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    required_fields = ["exercise", "sets", "reps", "weights", "auto_increment"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required routine fields"}), 400
    routine = Routine()
    routine.exercise = data["exercise"]
    routine.sets = data["sets"]
    routine.reps = data["reps"]
    routine.weights = ','.join(str(w) for w in data["weights"])
    routine.auto_increment = data["auto_increment"]
    routine.user_id = user.id
    db.session.add(routine)
    db.session.commit()
    return jsonify({"message": "Exercise added"})

@app.route("/api/routine/<username>/<int:rid>", methods=["PUT"])
def edit_routine(username, rid):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    routine = Routine.query.filter_by(id=rid, user_id=user.id).first()
    if not routine:
        return jsonify({"error": "Routine not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    routine.exercise = data.get("exercise", routine.exercise)
    routine.sets = data.get("sets", routine.sets)
    routine.reps = data.get("reps", routine.reps)
    if "weights" in data:
        routine.weights = ','.join(str(w) for w in data["weights"])
    routine.auto_increment = data.get("auto_increment", routine.auto_increment)
    db.session.commit()
    return jsonify({"message": "Exercise updated"})

@app.route("/api/routine/<username>/<int:rid>", methods=["DELETE"])
def delete_routine(username, rid):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    routine = Routine.query.filter_by(id=rid, user_id=user.id).first()
    if not routine:
        return jsonify({"error": "Routine not found"}), 404
    db.session.delete(routine)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"})

if __name__ == "__main__":
    # Ensure tables are created inside the app context
    with app.app_context():
        db.create_all()
    app.run(debug=True)