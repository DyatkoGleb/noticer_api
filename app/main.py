from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
from database import Database

app = FastAPI(
    title="Your API Title",
    description="Your API Description",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
)
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