from fastapi import FastAPI,HTTPException

from passlib.hash import bcrypt
from db import connect_db, disconnect_db,db

from routes import users
from routes import stories
from routes import drafts

import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace "*" with the frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routes
app.include_router(users.router)
app.include_router(stories.router, prefix="/stories", tags=["stories"])
app.include_router(drafts.router, prefix="/drafts", tags=["drafts"])