from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.context import CryptContext

import models
import schema
from config import TORTOISE_ORM

app = FastAPI()

pwd_context = CryptContext(schema=['bcrypt'], deprecated="auto")
User_Pydantic = pydantic_model_creator(models.User, name="User")
UserIn_Pydantic = pydantic_model_creator(models.User, name="UserIn", exclude_readonly=True)


@app.post('/register/', response_model=schema.User)
async def create_user(user: schema.UserCreate):
    user_obj = models.User(email=user.email, hashed_password=pwd_context.hash(user.password))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get('/users/{id}', response_model=schema.User)
async def get_user(id: int):
    user = await models.User.filter(id=id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await User_Pydantic.from_tortoise_orm(user)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
