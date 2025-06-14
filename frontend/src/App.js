import React, { useState, useEffect } from 'react';

function WeightsInput({ weights, setWeights }) {
  // Add a new weight input (default to last value or 0)
  const addWeight = () => setWeights([...weights, weights[weights.length - 1] || 0]);
  // Remove the last weight input
  const removeWeight = () => setWeights(weights.length > 1 ? weights.slice(0, -1) : [0]);
  // Update a specific weight
  const updateWeight = (idx, value) => {
    const newWeights = [...weights];
    newWeights[idx] = value;
    setWeights(newWeights);
  };

  return (
    <div>
      <label>Weight for Each Set:</label>
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

  // Workout state
  const [workoutMode, setWorkoutMode] = useState(false);
  const [workoutIdx, setWorkoutIdx] = useState(0);
  const [completedIds, setCompletedIds] = useState([]);

  // Always use normalized username for API calls
  const normalizedUsername = username.trim().toLowerCase();

  // Fetch routine after login or when updated
  useEffect(() => {
    if (loggedIn) {
      fetch(`http://localhost:5000/api/routine/${normalizedUsername}`)
        .then(res => res.json())
        .then(data => setRoutine(data));
    }
    // eslint-disable-next-line
  }, [loggedIn, normalizedUsername]);

  // Registration
  const register = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: normalizedUsername, password })
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
      setLoggedIn(true);
    }
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
        auto_increment: autoIncrement
      })
    });
    setExercise('');
    setSets(1);
    setReps(1);
    setWeights([0]);
    setAutoIncrement(0);
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
    await fetch(`http://localhost:5000/api/routine/${normalizedUsername}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exercise: newExercise,
        sets: Number(newSets),
        reps: Number(newReps),
        weights: newWeights.split(',').map(Number),
        auto_increment: Number(newAutoInc)
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

  // Auth UI
  if (!loggedIn) {
    return (
      <div>
        <h1>Register or Login</h1>
        <form onSubmit={register}>
          <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
          <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
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
    return (
      <div>
        <h1>Workout: {ex.exercise}</h1>
        <p>Sets: {ex.sets}, Reps: {ex.reps}</p>
        <p>Weights: {ex.weights.join(', ')} lbs</p>
        <button onClick={completeExercise}>
          {workoutIdx + 1 < routine.length ? "Next Exercise" : "Finish Workout"}
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

  return (
    <div>
      <h1>Your Routine</h1>
      {Array.isArray(routine) && routine.length === 0 ? (
        <p>No exercises yet. Add your first exercise below!</p>
      ) : (
        <ul>
          {Array.isArray(routine) && routine.map((ex, idx) => (
            <li key={ex.id || idx}>
              {ex.exercise}: {ex.sets} sets x {ex.reps} reps, Weights: {ex.weights.join(', ')} lbs, Auto-increment: {ex.auto_increment}
              <button onClick={() => editExercise(ex.id)}>Edit</button>
              <button onClick={() => deleteExercise(ex.id)}>Delete</button>
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
        />
        <br />
        <label>
          Auto-increment Weight (lbs/kg added after each workout)<br />
          <input
            type="number"
            value={autoIncrement}
            onChange={e => setAutoIncrement(Number(e.target.value))}
            placeholder="e.g. 5"
            style={{ width: 100, marginBottom: 8 }}
          />
        </label>
        <br />
        <button type="submit" style={{ marginTop: 8 }}>Add Exercise to Routine</button>
      </form>
      <button onClick={startWorkout} disabled={!Array.isArray(routine) || routine.length === 0}>Start Workout</button>
      {message && <p style={{ color: 'green' }}>{message}</p>}
    </div>
  );
}

export default App;