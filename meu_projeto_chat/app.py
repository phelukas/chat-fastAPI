# meu_projeto_chat/app.py

from fastapi import FastAPI

from fastapi.responses import RedirectResponse

from meu_projeto_chat.api.routes import user_routes

from meu_projeto_chat.api.router import auth_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(auth_routes.router)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
