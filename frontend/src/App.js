import React, { useState, useEffect } from 'react';

const PRESET_ROUTINES = [
  {
    name: "Full Body Beginner",
    exercises: [
      { exercise: "Squat", sets: 3, reps: 8, weights: [45, 45, 45], auto_increment: 5, routine_type: "bodybuilding" },
      { exercise: "Bench Press", sets: 3, reps: 8, weights: [45, 45, 45], auto_increment: 5, routine_type: "bodybuilding" },
      { exercise: "Deadlift", sets: 3, reps: 8, weights: [65, 65, 65], auto_increment: 10, routine_type: "bodybuilding" }
    ]
  },
  {
    name: "Push Day",
    exercises: [
      { exercise: "Bench Press", sets: 3, reps: 8, weights: [45, 45, 45], auto_increment: 5, routine_type: "bodybuilding" },
      { exercise: "Overhead Press", sets: 3, reps: 8, weights: [35, 35, 35], auto_increment: 5, routine_type: "bodybuilding" },
      { exercise: "Dumbbell Flies", sets: 3, reps: 8, weights: [15, 15, 15], auto_increment: 2, routine_type: "bodybuilding" }
    ]
  }
];

const PRESET_EXERCISES = [
  { label: "Squat 3x8", exercise: "Squat", sets: 3, reps: 8, weights: [45, 45, 45], auto_increment: 5, routine_type: "bodybuilding" },
  { label: "Bench Press 3x8", exercise: "Bench Press", sets: 3, reps: 8, weights: [45, 45, 45], auto_increment: 5, routine_type: "bodybuilding" },
  { label: "Dumbbell Flies 3x8", exercise: "Dumbbell Flies", sets: 3, reps: 8, weights: [15, 15, 15], auto_increment: 2, routine_type: "bodybuilding" }
];

function WeightsInput({ weights, setWeights, unit }) {
  const addWeight = () => setWeights([...weights, weights[weights.length - 1] || 0]);
  const removeWeight = () => setWeights(weights.length > 1 ? weights.slice(0, -1) : [0]);
  const updateWeight = (idx, value) => {
    const newWeights = [...weights];
    newWeights[idx] = value;
    setWeights(newWeights);
  };

  return (
    <div>
      <label>Weight for Each Set ({unit}):</label>
      {weights.map((w, idx) => (
        <div key={idx} style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
          <span>Set {idx + 1}:</span>
          <input
            type="number"
            value={w}
            min="0"
            step="1"
            style={{ width: 70, marginLeft: 8, marginRight: 8 }}
            onChange={e => updateWeight(idx, Number(e.target.value))}
            required
          />
          {weights.length > 1 && (
            <button type="button" onClick={removeWeight} title="Remove this set" style={{ marginLeft: 4 }}>-</button>
          )}
          {idx === weights.length - 1 && (
            <button type="button" onClick={addWeight} title="Add another set" style={{ marginLeft: 4 }}>+</button>
          )}
        </div>
      ))}
      <small>Use + to add a set, - to remove the last set.</small>
    </div>
  );
}

function plateCalculator(targetWeight, unit = "lb", barWeight = null) {
  let plateSizes, defaultBar;
  if (unit === "lb") {
    plateSizes = [45, 35, 25, 10, 5, 2.5, 1.25];
    defaultBar = 45;
  } else {
    plateSizes = [25, 20, 15, 10, 5, 2.5, 1.25, 0.5];
    defaultBar = 20;
  }
  barWeight = barWeight || defaultBar;
  if (targetWeight < barWeight) return { barOnly: true };
  let perSide = (targetWeight - barWeight) / 2;
  const result = {};
  for (const plate of plateSizes) {
    const count = Math.floor(perSide / plate);
    if (count > 0) {
      result[plate] = count;
      perSide -= plate * count;
    }
  }
  if (Math.round(perSide * 100) / 100 > 0) {
    result['unmatched'] = Math.round(perSide * 100) / 100;
  }
  return result;
}

function App() {
  // Auth state
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [message, setMessage] = useState('');

  // Routine state
  const [routine, setRoutine] = useState([]);
  const [exercise, setExercise] = useState('');
  const [sets, setSets] = useState(1);
  const [reps, setReps] = useState(1);
  const [weights, setWeights] = useState([0]);
  const [autoIncrement, setAutoIncrement] = useState(0);
  const [routineType, setRoutineType] = useState("bodybuilding");
  const [exerciseType, setExerciseType] = useState("barbell");

  // Workout state
  const [workoutMode, setWorkoutMode] = useState(false);
  const [workoutIdx, setWorkoutIdx] = useState(0);
  const [completedIds, setCompletedIds] = useState([]);

  // Unit state
  const [unit, setUnit] = useState("lb");

  // Add state to track success for each exercise
  const [successes, setSuccesses] = useState([]);

  // Preset routine picker state
  const [showPresetRoutinePicker, setShowPresetRoutinePicker] = useState(false);

  // New state variable for user settings menu
  const [showSettings, setShowSettings] = useState(false);

  // New state variable for exercise unit in add exercise form
  const [exerciseUnit, setExerciseUnit] = useState(unit); // default to user unit

  // New state variable for recommended weight increment
  const [recommendedIncrement, setRecommendedIncrement] = useState(2.5);

  // New state variable for exercise category
  const [exerciseCategory, setExerciseCategory] = useState("upper");

  // Always use normalized username for API calls
  const normalizedUsername = username.trim().toLowerCase();

  // Fetch routine and user info after login or when updated
  useEffect(() => {
    if (loggedIn) {
      fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
        .then(res => res.json())
        .then(data => {
          setRoutine(data);
          if (Array.isArray(data) && data.length === 0) {
            setShowPresetRoutinePicker(true);
          } else {
            setShowPresetRoutinePicker(false);
          }
        });
      fetch(`http://localhost:5000/api/user/${normalizedUsername}`)
        .then(res => res.json())
        .then(data => {
          if (data.unit) setUnit(data.unit);
        });
    }
    // eslint-disable-next-line
  }, [loggedIn, normalizedUsername]);

  // Registration
  const register = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: normalizedUsername, password, unit })
    });
    const data = await res.json();
    setMessage(data.message || data.error);
    if (data.message) {
      setUsername(normalizedUsername);
      setLoggedIn(true);
    }
  };

  // Login
  const login = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: normalizedUsername, password })
    });
    const data = await res.json();
    setMessage(data.message || data.error);
    if (data.message) {
      setUsername(normalizedUsername);
      setLoggedIn(true;
    }
  };

  // Toggle unit
  const toggleUnit = async () => {
    const newUnit = unit === "lb" ? "kg" : "lb";
    await fetch(`http://localhost:5000/api/user/${normalizedUsername}/unit`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unit: newUnit })
    });
    setUnit(newUnit);
    // Immediately refresh routine and user info after unit change
    fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
      .then(res => res.json())
      .then(data => setRoutine(data));
    fetch(`http://localhost:5000/api/user/${normalizedUsername}`)
      .then(res => res.json())
      .then(data => {
        if (data.unit) setUnit(data.unit);
      });
  };

  // Add Exercise
  const addExercise = async (e) => {
    e.preventDefault();
    await fetch(`http://localhost:5000/api/routine/${normalizedUsername}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exercise,
        sets,
        reps,
        weights,
        auto_increment: recommendedIncrement,
        routine_type: routineType,
        exercise_type: exerciseType,
        unit: exerciseUnit,
        category: exerciseCategory
      })
    });
    setExercise('');
    setSets(1);
    setReps(1);
    setWeights([0]);
    setAutoIncrement(0);
    setRoutineType("bodybuilding");
    setExerciseType("barbell");
    // Refresh routine
    fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
      .then(res => res.json())
      .then(data => setRoutine(data));
  };

  // Delete Exercise
  const deleteExercise = async (id) => {
    await fetch(`http://localhost:5000/api/routine/${normalizedUsername}/${id}`, {
      method: 'DELETE'
    });
    fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
      .then(res => res.json())
      .then(data => setRoutine(data));
  };

  // Edit Exercise (simple version: prompt for new values)
  const editExercise = async (id) => {
    const newExercise = prompt("New exercise name:");
    const newSets = prompt("New sets:");
    const newReps = prompt("New reps:");
    const newWeights = prompt("New weights (comma separated):");
    const newAutoInc = prompt("New auto-increment:");
    const newRoutineType = prompt("Routine type (bodybuilding/powerlifting):", "bodybuilding");
    await fetch(`http://localhost:5000/api/routine/${normalizedUsername}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exercise: newExercise,
        sets: Number(newSets),
        reps: Number(newReps),
        weights: newWeights.split(',').map(Number),
        auto_increment: Number(newAutoInc),
        routine_type: newRoutineType
      })
    });
    fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
      .then(res => res.json())
      .then(data => setRoutine(data));
  };

  // Start Workout
  const startWorkout = () => {
    setWorkoutMode(true);
    setWorkoutIdx(0);
    setCompletedIds([]);
  };

  // Complete current exercise in workout
  const completeExercise = () => {
    setCompletedIds([...completedIds, routine[workoutIdx].id]);
    if (workoutIdx + 1 < routine.length) {
      setWorkoutIdx(workoutIdx + 1);
    } else {
      // End workout, call backend to auto-increment weights
      fetch(`http://localhost:5000/api/workout/${normalizedUsername}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: completedIds.concat(routine[workoutIdx].id) })
      }).then(res => res.json())
        .then(data => {
          setMessage(data.message);
          setWorkoutMode(false);
          // Refresh routine
          fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
            .then(res => res.json())
            .then(data => setRoutine(data));
        });
    }
  };

  // Delete Account
  const handleDeleteAccount = async () => {
    const confirm = window.confirm("Are you sure you want to delete your account? This cannot be undone.");
    if (!confirm) return;
    const pwd = prompt("Please enter your password to confirm:");
    if (!pwd) return;
    const res = await fetch(`http://localhost:5000/api/user/${normalizedUsername}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: pwd })
    });
    const data = await res.json();
    if (data.message) {
      alert("Account deleted.");
      setLoggedIn(false);
      setUsername("");
      setPassword("");
      setRoutine([]);
    } else {
      alert(data.error || "Failed to delete account.");
    }
  };

  // Auth UI
  if (!loggedIn) {
    return (
      <div>
        <h1>Register or Login</h1>
        <form onSubmit={register}>
          <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
          <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
          <label>
            Weight Unit<br />
            <select value={unit} onChange={e => setUnit(e.target.value)} required>
              <option value="lb">Pounds (lb)</option>
              <option value="kg">Kilograms (kg)</option>
            </select>
          </label>
          <br />
          <button type="submit">Register</button>
        </form>
        <form onSubmit={login}>
          <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
          <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
          <button type="submit">Login</button>
        </form>
        <p>{message}</p>
      </div>
    );
  }

  // Workout UI
  if (workoutMode && Array.isArray(routine) && routine.length > 0) {
    const ex = routine[workoutIdx];
    const weight = ex.weights[0];
    const plates = plateCalculator(weight, unit);

    const handleExerciseResult = (success) => {
      const updatedSuccesses = [...successes, { id: ex.id, success }];
      if (workoutIdx + 1 < routine.length) {
        setSuccesses(updatedSuccesses);
        setWorkoutIdx(workoutIdx + 1);
      } else {
        // Only send successful exercise IDs to backend for increment
        const completed = updatedSuccesses.filter(s => s.success).map(s => s.id);
        fetch(`http://localhost:5000/api/workout/${normalizedUsername}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed })
        }).then(res => res.json())
          .then(data => {
            setMessage(data.message);
            setWorkoutMode(false);
            setSuccesses([]);
            fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
              .then(res => res.json())
              .then(data => setRoutine(data));
          });
      }
    };

    return (
      <div>
        <h1>Workout: {ex.exercise}</h1>
        <p>Sets: {ex.sets}, Reps: {ex.reps}</p>
        <p>Weight: {weight} {unit}</p>
        <div>
          <strong>Plate breakdown per side:</strong>
          {plates.barOnly ? (
            <div>Use bar only</div>
          ) : (
            <ul>
              {Object.entries(plates).map(([plate, count]) =>
                plate !== 'unmatched' ? (
                  <li key={plate}>{count} × {plate} {unit} plate{count > 1 ? 's' : ''}</li>
                ) : (
                  <li key="unmatched" style={{ color: 'red' }}>
                    Unmatched: {count} {unit} (cannot be loaded with standard plates)
                  </li>
                )
              )}
            </ul>
          )}
        </div>
        <button onClick={() => handleExerciseResult(true)}>
          {workoutIdx + 1 < routine.length ? "Completed - Next Exercise" : "Completed - Finish Workout"}
        </button>
        <button onClick={() => handleExerciseResult(false)} style={{ marginLeft: 8 }}>
          {workoutIdx + 1 < routine.length ? "Failed - Next Exercise" : "Failed - Finish Workout"}
        </button>
      </div>
    );
  }

  // Main UI
  if (routine && routine.error) {
    return (
      <div>
        <h1>Your Routine</h1>
        <p style={{ color: 'red' }}>{routine.error}</p>
        <button onClick={() => setLoggedIn(false)}>Back to Login</button>
        <p>{message}</p>
      </div>
    );
  }

  if (showPresetRoutinePicker) {
    return (
      <div>
        <h2>Pick a Preset Routine or Start from Scratch</h2>
        {PRESET_ROUTINES.map((preset, idx) => (
          <div key={idx} style={{ border: "1px solid #ccc", margin: 8, padding: 8 }}>
            <strong>{preset.name}</strong>
            <ul>
              {preset.exercises.map((ex, i) => (
                <li key={i}>{ex.exercise}: {ex.sets}x{ex.reps} ({ex.weights.join(", ")} {unit})</li>
              ))}
            </ul>
            <button onClick={async () => {
              // Add all preset exercises to user's routine
              for (const ex of preset.exercises) {
                await fetch(`http://localhost:5000/api/routine/${normalizedUsername}`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(ex)
                });
              }
              // Refresh routine and hide picker
              fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
                .then(res => res.json())
                .then(data => {
                  setRoutine(data);
                  setShowPresetRoutinePicker(false);
                });
            }}>Add This Routine</button>
          </div>
        ))}
        <button onClick={() => setShowPresetRoutinePicker(false)}>Start from Scratch</button>
      </div>
    );
  }

  return (
    <div>
      <h1>Your Routine</h1>
      <button onClick={() => setShowSettings(true)} style={{ marginBottom: 8 }}>
        User Settings
      </button>
      {showSettings && (
        <div style={{ border: "1px solid #ccc", padding: 16, background: "#fff", position: "absolute", zIndex: 10 }}>
          <h2>User Settings</h2>
          <button onClick={toggleUnit}>
            Switch all exercises to {unit === "lb" ? "kg" : "lb"}
          </button>
          <button onClick={() => setShowSettings(false)} style={{ marginLeft: 8 }}>Close</button>
        </div>
      )}
      <button onClick={toggleUnit} style={{ marginBottom: 8 }}>
        Switch to {unit === "lb" ? "kg" : "lb"}
      </button>
      {Array.isArray(routine) && routine.length === 0 ? (
        <p>No exercises yet. Add your first exercise below!</p>
      ) : (
        <ul>
          {Array.isArray(routine) && routine.map((ex, idx) => (
            <li key={ex.id || idx}>
              {ex.exercise} ({ex.routine_type || "bodybuilding"}): {ex.sets} sets x {ex.reps} reps, Weights: {ex.weights.join(', ')} {ex.unit || unit}, Auto-increment: {ex.auto_increment}
              <button onClick={() => editExercise(ex.id)}>Edit</button>
              <button onClick={() => deleteExercise(ex.id)}>Delete</button>
              <button onClick={async () => {
                const newUnit = (ex.unit || unit) === "lb" ? "kg" : "lb";
                await fetch(`http://localhost:5000/api/routine/${normalizedUsername}/${ex.id}/unit`, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ unit: newUnit })
                });
                fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
                  .then(res => res.json())
                  .then(data => setRoutine(data));
              }}>
                Swap to {(ex.unit || unit) === "lb" ? "kg" : "lb"}
              </button>
            </li>
          ))}
        </ul>
      )}
      <h2>Add Exercise</h2>
      <form onSubmit={addExercise} style={{ border: '1px solid #ccc', padding: 16, borderRadius: 8, maxWidth: 400 }}>
        <label>
          Exercise Name<br />
          <input
            value={exercise}
            onChange={e => setExercise(e.target.value)}
            placeholder="e.g. Squat"
            required
            style={{ width: '100%', marginBottom: 8 }}
          />
        </label>
        <br />
        <label>
          Number of Sets<br />
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
            <button type="button" onClick={() => setSets(Math.max(1, sets - 1))} style={{ width: 30 }}>-</button>
            <input
              type="number"
              value={sets}
              min="1"
              max="20"
              step="1"
              onChange={e => setSets(Number(e.target.value))}
              required
              style={{ width: 60, textAlign: 'center', margin: '0 8px' }}
            />
            <button type="button" onClick={() => setSets(sets + 1)} style={{ width: 30 }}>+</button>
          </div>
        </label>
        <label>
          Number of Reps per Set<br />
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
            <button type="button" onClick={() => setReps(Math.max(1, reps - 1))} style={{ width: 30 }}>-</button>
            <input
              type="number"
              value={reps}
              min="1"
              max="50"
              step="1"
              onChange={e => setReps(Number(e.target.value))}
              required
              style={{ width: 60, textAlign: 'center', margin: '0 8px' }}
            />
            <button type="button" onClick={() => setReps(reps + 1)} style={{ width: 30 }}>+</button>
          </div>
        </label>
        <WeightsInput
          weights={weights.length === sets ? weights : Array(sets).fill(0).map((_, i) => weights[i] || 0)}
          setWeights={w => setWeights(w.length === sets ? w : Array(sets).fill(0).map((_, i) => w[i] || 0))}
          unit={unit}
        />
        <br />
        <label>
          Auto-increment Weight ({unit} added after each workout)<br />
          <input
            type="number"
            value={autoIncrement}
            onChange={e => setAutoIncrement(Number(e.target.value))}
            placeholder="e.g. 5"
            style={{ width: 100, marginBottom: 8 }}
          />
        </label>
        <br />
        <label>
          Routine Type<br />
          <select value={routineType} onChange={e => setRoutineType(e.target.value)} required>
            <option value="bodybuilding">Bodybuilding</option>
            <option value="powerlifting">Powerlifting</option>
          </select>
        </label>
        <br />
        <label>
          Exercise Type<br />
          <select value={exerciseType} onChange={e => setExerciseType(e.target.value)} required>
            <option value="barbell">Barbell</option>
            <option value="dumbbell">Dumbbell</option>
            <option value="bodyweight">Bodyweight</option>
          </select>
        </label>
        <br />
        <label>
          Exercise Unit<br />
          <select value={exerciseUnit} onChange={e => setExerciseUnit(e.target.value)} required>
            <option value="lb">Pounds (lb)</option>
            <option value="kg">Kilograms (kg)</option>
          </select>
        </label>
        <label>
          Exercise Category<br />
          <select value={exerciseCategory} onChange={e => setExerciseCategory(e.target.value)} required>
            <option value="arms">Arms</option>
            <option value="legs">Legs</option>
            <option value="chest">Chest</option>
            <option value="back">Back</option>
            <option value="upper">Upper Body</option>
            <option value="lower">Lower Body</option>
          </select>
        </label>
        <div>
          <span>Recommended Increment: </span>
          {exerciseUnit === "lb" ? (
            <>
              <button type="button" onClick={() => setRecommendedIncrement(2.5)}>2.5 lb (upper body)</button>
              <button type="button" onClick={() => setRecommendedIncrement(5)}>5 lb (lower body)</button>
            </>
          ) : (
            <>
              <button type="button" onClick={() => setRecommendedIncrement(1.25)}>1.25 kg (upper body)</button>
              <button type="button" onClick={() => setRecommendedIncrement(2.5)}>2.5 kg (lower body)</button>
            </>
          )}
          <span style={{ marginLeft: 8 }}>Current: {recommendedIncrement} {exerciseUnit}</span>
        </div>
        <br />
        <button type="submit" style={{ marginTop: 8 }}>Add Exercise to Routine</button>
      </form>
      <button onClick={startWorkout} disabled={!Array.isArray(routine) || routine.length === 0}>Start Workout</button>
      <button onClick={handleDeleteAccount} style={{ color: "red", marginTop: 16 }}>Delete My Account</button>
      {message && <p style={{ color: 'green' }}>{message}</p>}

      {/* Preset Routine Picker */}
      {showPresetRoutinePicker && (
        <div style={{ marginTop: 32, padding: 16, border: '1px solid #ccc', borderRadius: 8, maxWidth: 400 }}>
          <h2>Select a Preset Routine</h2>
          {PRESET_ROUTINES.map(r => (
            <div key={r.name} style={{ marginBottom: 16 }}>
              <h3>{r.name}</h3>
              <ul>
                {r.exercises.map((ex, idx) => (
                  <li key={idx}>
                    {ex.exercise}: {ex.sets} sets x {ex.reps} reps, Weights: {ex.weights.join(', ')} {unit}
                  </li>
                ))}
              </ul>
              <button onClick={async () => {
                // Add each exercise in the preset routine to the user's routine
                for (const ex of r.exercises) {
                  await fetch(`http://localhost:5000/api/routine/${normalizedUsername}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      exercise: ex.exercise,
                      sets: ex.sets,
                      reps: ex.reps,
                      weights: ex.weights,
                      auto_increment: ex.auto_increment,
                      routine_type: ex.routine_type
                    })
                  });
                }
                // Refresh routine and close picker
                fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
                  .then(res => res.json())
                  .then(data => setRoutine(data));
                setShowPresetRoutinePicker(false);
              }}>
                Select This Routine
              </button>
            </div>
          ))}
          <button onClick={() => setShowPresetRoutinePicker(false)} style={{ marginTop: 8 }}>
            Cancel
          </button>
        </div>
      )}
      <h3>Or add a preset exercise:</h3>
      <div style={{ marginBottom: 12 }}>
        {PRESET_EXERCISES.map((preset, idx) => (
          <button key={idx} style={{ marginRight: 8, marginBottom: 8 }} onClick={async () => {
            await fetch(`http://localhost:5000/api/routine/${normalizedUsername}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(preset)
            });
            fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
              .then(res => res.json())
              .then(data => setRoutine(data));
          }}>
            {preset.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default App;