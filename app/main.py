from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
from database.database import Database

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

Database().create_tables()