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
    weights = db.Column(db.String(120), nullable=False)
    auto_increment = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    routine_type = db.Column(db.String(32), default="bodybuilding")  # "bodybuilding" or "powerlifting"


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    if not data or "username" not in data or "password" not in data or "unit" not in data:
        return jsonify({"error": "Username, password, and unit are required"}), 400
    username = data["username"].strip().lower()
    password = data["password"]
    unit = data["unit"]
    if unit not in ("lb", "kg"):
        return jsonify({"error": "Unit must be 'lb' or 'kg'"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    user = User()
    user.username = username
    user.password = password
    user.unit = unit
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"})

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
            "weights": [float(w) for w in r.weights.split(',')],
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
    routine.weights = ','.join(str(float(w)) for w in data["weights"])
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
        routine.weights = ','.join(str(float(w)) for w in data["weights"])
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

@app.route("/api/workout/<username>", methods=["POST"])
def start_workout(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    completed = data.get("completed", [])
    for rid in completed:
        routine = Routine.query.filter_by(id=rid, user_id=user.id).first()
        if routine and routine.auto_increment > 0:
            weights = [int(w) + routine.auto_increment for w in routine.weights.split(',')]
            routine.weights = ','.join(str(w) for w in weights)
    db.session.commit()
    return jsonify({"message": "Workout complete, weights updated."})

@app.route("/api/user/<username>/unit", methods=["PUT"])
def update_unit(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    if not data or "unit" not in data:
        return jsonify({"error": "Unit is required"}), 400
    new_unit = data.get("unit")
    if new_unit not in ("lb", "kg"):
        return jsonify({"error": "Unit must be 'lb' or 'kg'"}), 400
    if user.unit == new_unit:
        return jsonify({"message": "Unit unchanged", "unit": user.unit})

    # Conversion and rounding to real-world plate increments
    def round_to_lb_plate(x):
        return round(x / 2.5) * 2.5

    def round_to_kg_plate(x):
        return round(x / 1.25) * 1.25

    def lb_to_kg(lb):
        return round_to_kg_plate(lb * 0.453592)

    def kg_to_lb(kg):
        return round_to_lb_plate(kg / 0.453592)

    for routine in user.routines:
        weights = [float(w) for w in routine.weights.split(',')]
        if user.unit == "lb" and new_unit == "kg":
            weights = [lb_to_kg(w) for w in weights]
        elif user.unit == "kg" and new_unit == "lb":
            weights = [kg_to_lb(w) for w in weights]
        routine.weights = ','.join(str(w) for w in weights)
    user.unit = new_unit
    db.session.commit()
    return jsonify({"message": "Unit updated and weights converted", "unit": user.unit})

@app.route("/api/user/<username>", methods=["DELETE"])
def delete_account(username):
    data = request.json
    if not data or "password" not in data:
        return jsonify({"error": "Password is required"}), 400
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid credentials"}), 401
    # Delete all routines first
    Routine.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"})

@app.route("/api/user/<username>", methods=["GET"])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "username": user.username,
        "unit": user.unit,
        "goal": user.goal
    })

if __name__ == "__main__":
    # Ensure tables are created inside the app context
    with app.app_context():
        db.create_all()
    app.run(debug=True)