from fastapi import APIRouter, Request
from controllers import NoteController
from models import Note, Todo, Notice

router = APIRouter()


@router.post("/addNewNote")
def add_new_note(note: dict):
    return NoteController().save_note_action(note)

@router.get("/getNotes")
def get_notes(request: Request):
    return NoteController().get_notes_action(request)

@router.post("/editNote")
def edit_note(note: dict):
    return NoteController().save_updated_note_action(note)

@router.post("/deleteNote")
async def delete_note(note: dict):
    return NoteController().delete_note_action(Note, note)

@router.get("/getTodos")
def get_todos(request: Request):
    return NoteController().get_todos_action(request)

@router.post("/deleteTodo")
async def delete_todo(todo: dict):
    return NoteController().delete_note_action(Todo, todo)

@router.get("/getAllNotices")
def get_all_notices(request: Request):
    return NoteController().get_all_notices_action(request)

@router.get("/getCurrentNotices")
def get_current_notices(request: Request):
    return NoteController().get_current_notices_action(request)

@router.post("/deleteNotice")
def delete_notice(notice: dict):
    return NoteController().delete_note_action(Notice, notice)
