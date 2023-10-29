from fastapi import APIRouter, Request
from controllers import NoteController

router = APIRouter()


@router.post("/addNewNote")
def add_new_note(note: dict):
    return NoteController().save_note_action(note)

@router.post("/deleteNote")
def get_notes(note: dict):
    return NoteController().delete_note_action(note)

@router.get("/getNotes")
def get_notes(request: Request):
    return NoteController().get_notes_action(request)

@router.get("/getTodos")
def get_notes(request: Request):
    return NoteController().get_todos_action(request)

@router.get("/getAllNotices")
def get_notices(request: Request):
    return NoteController().get_all_notices_action(request)

@router.get("/getCurrentNotices")
def get_notices(request: Request):
    return NoteController().get_current_notices_action(request)

@router.post("/deleteNotice")
def get_notes(note: dict):
    return NoteController().delete_notice_action(note)
