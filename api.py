from fastapi import FastAPI,HTTPException

from prisma import Prisma
from passlib.hash import bcrypt
from db import connect_db, disconnect_db,db

from routes import users

import os
from langchain_openai import ChatOpenAI

app = FastAPI()
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",   # your site url (for rate-limits/tracking)
        "X-Title": "Storytelling AI Bot",     # project name
    }
)

# Include routes
app.include_router(users.router)
