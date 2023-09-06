from fastapi import APIRouter
from controllers.new_note_controller import NewNoteController

router = APIRouter()


@router.post("/addNewNote")
async def add_new_note(note: dict):
    return NewNoteController().save_note_action(note)
