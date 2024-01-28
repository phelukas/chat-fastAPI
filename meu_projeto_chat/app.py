# meu_projeto_chat/app.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from meu_projeto_chat.api.routes import user_routes
from meu_projeto_chat.api.routes import auth_routes
from meu_projeto_chat.api.routes import chat_room

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(chat_room.router)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
