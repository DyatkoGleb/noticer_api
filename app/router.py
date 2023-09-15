from fastapi import APIRouter, Request
from controllers import NoteController

router = APIRouter()


@router.post("/addNewNote")
def add_new_note(note: dict):
    return NoteController().save_note_action(note)

@router.get("/getNotes")
def get_notes(request: Request):
    return NoteController().get_notes_action(request)

@router.get("/getNotices")
def get_notices(request: Request):
    return NoteController().get_notices_action(request)
