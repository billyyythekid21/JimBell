from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from pwdlib import PasswordHash

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class Workout(BaseModel):
    id: int
    user_id: int
    name: str
    duration_minutes: int

workouts: List[Workout] = []
users: List[User] = []

@app.get("/")
def root():
    return {"message": "JimBell API is running!"}

@app.post("/users/signup")
def signup(user: User):
    for u in users:
        if u.username == user.username:
            raise HTTPException(status_code=400, detail="ERROR: Username " \
            "   already exists!")
        elif u.email == user.email:
            raise HTTPException(status_code=400, detail="ERROR: Email " \
            "   already exists!")
    users.append(user)
    return {"message": "User signed up successfully", "user": user}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/users/login")
def login(request: LoginRequest):
    for u in users:
        if u.username == request.username and u.password == request.password:
            return {"message": f"Login successful for {u.username}"}
    raise HTTPException(status_code=401, detail="ERROR: Invalid username "
        "or password")

@app.get("/workouts")
def get_workouts(user_id: int = Query(..., description="User ID")):
    user_workouts = [w for w in workouts if w.user_id == user_id]
    return user_workouts

@app.post("/workouts")
def add_workout(workout: Workout):
    if not any(u.id == workout.user_id for u in users):
        raise HTTPException(status_code=400, detail="ERROR: User does not exist")
    workouts.append(workout)
    return workout

@app.put("/workouts/{workout_id}")
def update_workout(workout_id: int, updated: Workout):
    for i, workout in enumerate(workouts):
        if workout.id == workout_id:
            if not any(u.id == updated.user_id for u in users):
                raise HTTPException(status_code=400, detail="ERROR: User does not exist")
            workouts[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="ERROR: Workout not found")

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int):
    for i, workout in enumerate(workouts):
        if workout.id == workout_id:
            del workouts[i]
            return {"message": "Workout deleted"}
    raise HTTPException(status_code=404, detail="ERROR: Workout not found")