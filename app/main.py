from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

string_notice_date_length = 18

@app.post("/")
async def new_item(item: dict):
    if save_item(item):
        return 1
    else:
        return 2

def save_item(item: dict) -> bool:
    item_type = get_item_type(item['message'])
    text = get_text(item['message'], item_type)

    return save(text, item_type)

def get_item_type(text: str) -> str:
    if re.compile("^\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}").search(text):
        return 'notice'

    return 'note'

def get_text(message: str, type: str) -> str:
    if type == 'notice':
        return message[string_notice_date_length:]

    return message

def save(text: str, item_type: str) -> bool:



    return True