from fastapi import APIRouter, Request
from controllers.new_note_controller import NewNoteController

router = APIRouter()


@router.post("/addNewNote")
def add_new_note(note: dict):
    return NewNoteController().save_note_action(note)

@router.get("/getNotes")
def get_notes(request: Request):
    return NewNoteController().get_notes_action(request)

@router.get("/getNotices")
def get_notices(request: Request):
    return NewNoteController().get_notices_action(request)
