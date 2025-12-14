from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import cmd, users, login, ticket, event

app = FastAPI()

api_router = APIRouter()
api_router.include_router(cmd.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(ticket.router)
api_router.include_router(event.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)