from fastapi import APIRouter, Request
from controllers import NoteController

router = APIRouter()


@router.post("/addNewNote")
def add_new_note(note: dict):
    return NoteController().save_note_action(note)

@router.get("/getNotes")
def get_notes(request: Request):
    return NoteController().get_notes_action(request)

@router.post("/deleteNote")
async def get_notes(request: Request):
    return NoteController().delete_note_action(await request.json())

@router.get("/getTodos")
def get_notes(request: Request):
    return NoteController().get_todos_action(request)
@router.post("/deleteTodo")
async def get_notes(request: Request):
    return NoteController().delete_todo_action(await request.json())

@router.get("/getAllNotices")
def get_notices(request: Request):
    return NoteController().get_all_notices_action(request)

@router.get("/getCurrentNotices")
def get_notices(request: Request):
    return NoteController().get_current_notices_action(request)

@router.post("/deleteNotice")
async def get_notes(request: Request):
    return NoteController().delete_notice_action(await request.json())
