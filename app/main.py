from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import database.create as dbCreate
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

TYPE_NOTE = 'note'
TYPE_NOTICE = 'notice'
STRING_NOTICE_DATE_LENGTH = 16
OFFSET_STRING_NOTICE_DATE_LENGTH = STRING_NOTICE_DATE_LENGTH + 1


@app.post("/")
async def new_item(item: dict):
    if not item['message']:
        return {'success': False}

    return save_item(item)

def save_item(item: dict) -> bool:
    item_type = get_item_type(item['message'])
    text = get_text(item['message'], item_type)
    notice_datetime = None

    if item_type == TYPE_NOTICE:
        notice_datetime = get_notice_datetime(item['message'])

    return save(text, item_type, notice_datetime)

def get_item_type(text: str) -> str:
    if re.compile("^\d{1,2}.\d{2}.\d{4}\s\d{2}:\d{2}").search(text):
        return 'notice'

    return 'note'

def get_notice_datetime(message: str) -> datetime:
    date_string = message[:STRING_NOTICE_DATE_LENGTH]

    date_format = "%d.%m.%Y %H:%M"

    return datetime.strptime(date_string, date_format)

def get_text(message: str, type: str) -> str:
    if type == 'notice':
        return message[OFFSET_STRING_NOTICE_DATE_LENGTH:]

    return message

def save(text: str, item_type: str, datetime: datetime) -> bool:
    return dbCreate.Database().add_new_item(make_new_db_item(text, item_type, datetime))

def make_new_db_item(text: str, item_type: str, datetime: datetime) -> dbCreate.Notes | dbCreate.Notices:
    db_item = None

    note = {'text': text}

    if item_type == TYPE_NOTE:
        db_item = dbCreate.Notes(**note)
    elif item_type == TYPE_NOTICE:
        note['datetime'] = datetime
        db_item = dbCreate.Notices(**note)

    return db_item