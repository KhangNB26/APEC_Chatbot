from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend import chatbot

"""Main entry point for the APEC Chatbot application."""

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui"), name="ui")
app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])