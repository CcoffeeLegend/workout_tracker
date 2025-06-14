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

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(120), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weights = db.Column(db.String(120), nullable=False)  # Store as comma-separated string
    auto_increment = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Remove the old create_tables() and its call

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

if __name__ == "__main__":
    # Ensure tables are created inside the app context
    with app.app_context():
        db.create_all()
    app.run(debug=True)