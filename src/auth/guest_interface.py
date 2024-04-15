from fastapi import APIRouter, Form
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.oauth2 import *


router = APIRouter(
    tags=["guest"]
)
hashed = PasswordManager()
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/signup")
async def signup(
        response: Response,
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    response.status_code = 200
    try:
        async with get_async_session() as session:
            user_data = await find_user_by_nickname(session, username)
            mail_find = await find_user_by_email(session, email)
            if user_data:
                response.status_code = 208
            elif mail_find:
                response.status_code = 401
                return JSONResponse(content={"description": "This mail is registered"})
            else:
                user_id = await add_user(name,
                                         username,
                                         email,
                                         hashed.hash_password(password),
                                         "user",
                                         session)
            return JSONResponse(content={"description": "You're registered"})
    except:
        response.status_code = 500
        return JSONResponse(content={"description": "Внутренняя ошибка сервера"})


@router.post("/access_token")
async def token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends()
):
    username = form_data.username
    password = form_data.password
    users = await authenticate_user(username, password)
    if not users:
        response.status_code = 401
        return {"description": "Пользователь не авторизован"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}
