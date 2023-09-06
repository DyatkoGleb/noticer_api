from fastapi import APIRouter
from services.note_message_parser_service import NoteMessageParserService
from response.error_response import ErrorResponse
from response.success_response import SuccessResponse
from controllers.new_note_controller import NewNoteController

router = APIRouter()


@router.post("/addNewNote")
async def add_new_note(item: dict):
    entity = NoteMessageParserService().get_entity(item)

    if 'error' in entity:
        return ErrorResponse(entity['error']).get()

    return SuccessResponse(NewNoteController().save_item_action(entity))

