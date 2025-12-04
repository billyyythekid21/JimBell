from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    password: str

    workouts: List["Workout"] = Relationship(back_populates="owner")


class Workout(SQLModel, table=True):
    __tablename__ = "workouts"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    duration_minutes: int
    user_id: int = Field(foreign_key="users.id")

    owner: Optional[User] = Relationship(back_populates="workouts")