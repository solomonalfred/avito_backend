from uvicorn import Config, Server
import asyncio
from fastapi import FastAPI

import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')
    )
)
from src.db.guest_requests import *
from src.dependencies.hasher import *
from src.configuration import ADMIN_NAME, ADMIN_PASS, ADMIN_NICKNAME
from src.client import client_interface
from src.auth import guest_interface


app = FastAPI(
    title="Сервис баннеров",
    version="1.0.0",
)
hashed = PasswordManager()
app.include_router(client_interface.router)
app.include_router(guest_interface.router)


async def start():
    async with get_async_session() as session:
        await add_user_if_not_exists(session,
                                     ADMIN_NAME,
                                     ADMIN_NICKNAME,
                                     "nik_bogdanov2002@mail.ru",
                                     hashed.hash_password(ADMIN_PASS),
                                     "admin")

@app.on_event("startup")
async def startup_event():
    await start()


if __name__ == "__main__":
    config = Config(
        app=app,
        host="0.0.0.0",
        port=7777
    )
    server = Server(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())