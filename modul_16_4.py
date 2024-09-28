from fastapi import FastAPI, Path,Body,HTTPException
from typing import Annotated


from pydantic import BaseModel,validator


app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None

    @validator("username")
    def check_username(cls,value):
        if 5 <= len(value) <= 20:
            return value
        else:
            raise ValueError("Длина имени от 5 до 20 знаков")

    @validator("age")
    def check_age(cls, value):

        if 18 <= value <= 120:
            return value
        else:
            raise ValueError("Возраст от 18 до 120 лет")

@app.get("/users")
async def users_all() -> list[User]:
    return users



@app.post("/user/{username}/{age}")
async def user_add(user: User) ->str:
    user.id = len(users)+1
    users.append(user)
    return f"User {user} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def user_update(user_id: Annotated[ int,Path(ge=1, le=100, description="Enter User ID", example="10")],
                      username: Annotated[ str,Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                      age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    try:
        user = [i for i in users if i.id == user_id][0]
        user.username = username
        user.age = age
        return f"User {user} has been updated"
    except IndexError:
        raise HTTPException(status_code=404,detail="Index not found")



@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example="10")) -> str:
    try:
        user = [i for i in users if i.id == user_id][0]
        users.remove(user)
        return f"User {user} has been deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="Index not found")
