import React, { useState, useEffect } from 'react';

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

  // Fetch routine after login or when updated
  useEffect(() => {
    if (loggedIn) {
      fetch(`http://localhost:5000/api/routine/${username}`)
        .then(res => res.json())
        .then(data => setRoutine(data));
    }
  }, [loggedIn, username]);

  // Registration
  const register = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    setMessage(data.message || data.error);
    if (data.message) setLoggedIn(true);
  };

  // Login
  const login = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    setMessage(data.message || data.error);
    if (data.message) setLoggedIn(true);
  };

  // Add Exercise
  const addExercise = async (e) => {
    e.preventDefault();
    await fetch(`http://localhost:5000/api/routine/${username}`, {
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
    fetch(`http://localhost:5000/api/routine/${username}`)
      .then(res => res.json())
      .then(data => setRoutine(data));
  };

  // Delete Exercise
  const deleteExercise = async (id) => {
    await fetch(`http://localhost:5000/api/routine/${username}/${id}`, {
      method: 'DELETE'
    });
    fetch(`http://localhost:5000/api/routine/${username}`)
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
    await fetch(`http://localhost:5000/api/routine/${username}/${id}`, {
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
    fetch(`http://localhost:5000/api/routine/${username}`)
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
      fetch(`http://localhost:5000/api/workout/${username}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: completedIds.concat(routine[workoutIdx].id) })
      }).then(res => res.json())
        .then(data => {
          setMessage(data.message);
          setWorkoutMode(false);
          // Refresh routine
          fetch(`http://localhost:5000/api/routine/${username}`)
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
  if (workoutMode && routine.length > 0) {
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
  return (
    <div>
      <h1>Your Routine</h1>
      <ul>
        {routine.map((ex, idx) => (
          <li key={ex.id}>
            {ex.exercise}: {ex.sets} sets x {ex.reps} reps, Weights: {ex.weights.join(', ')} lbs, Auto-increment: {ex.auto_increment}
            <button onClick={() => editExercise(ex.id)}>Edit</button>
            <button onClick={() => deleteExercise(ex.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <h2>Add Exercise</h2>
      <form onSubmit={addExercise}>
        <input value={exercise} onChange={e => setExercise(e.target.value)} placeholder="Exercise" required />
        <input type="number" value={sets} onChange={e => setSets(Number(e.target.value))} min="1" placeholder="Sets" required />
        <input type="number" value={reps} onChange={e => setReps(Number(e.target.value))} min="1" placeholder="Reps" required />
        <input type="text" value={weights.join(',')} onChange={e => setWeights(e.target.value.split(',').map(Number))} placeholder="Weights (comma separated)" required />
        <input type="number" value={autoIncrement} onChange={e => setAutoIncrement(Number(e.target.value))} placeholder="Auto-increment" />
        <button type="submit">Add</button>
      </form>
      <button onClick={startWorkout} disabled={routine.length === 0}>Start Workout</button>
      <p>{message}</p>
    </div>
  );
}

export default App;