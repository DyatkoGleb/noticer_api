import sys
from fastapi import APIRouter
from services.note_message_parser import NoteMessageParser
from response.error_response import ErrorResponse
from response.success_response import SuccessResponse
from database import create as createDB
from constants import TYPE_NOTE, TYPE_NOTICE

sys.path.append('/')

router = APIRouter()


@router.post("/addNewNote")
async def add_new_note(item: dict):
    entity = NoteMessageParser().get_entity(item)

    if'error' in entity:
        return ErrorResponse(entity['error']).get()

    return SuccessResponse(save_item(entity))

def save_item(entity) -> dict:
    return createDB.Database().add_new_item(make_new_db_item(entity))

def make_new_db_item(entity: dict) -> createDB.Notes | createDB.Notices:
    db_item = None

    note = {'text': entity['text']}

    if entity['item_type'] == TYPE_NOTE:
        db_item = createDB.Notes(**note)
    elif entity['item_type'] == TYPE_NOTICE:
        note['datetime'] = entity['notice_datetime']
        db_item = createDB.Notices(**note)

    return db_item