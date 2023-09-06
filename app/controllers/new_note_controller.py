import sys
from constants import TYPE_NOTICE
from models.note import Note
from models.notice import Notice
from services.note_message_parser_service import NoteMessageParserService
from response.error_response import ErrorResponse
from response.success_response import SuccessResponse

sys.path.append('../')


class NewNoteController:
    def save_note_action(self, note: dict) -> SuccessResponse | ErrorResponse:
        entity = NoteMessageParserService().get_entity(note)

        if 'error' in entity:
            return ErrorResponse(entity['error']).get()

        try:
            return SuccessResponse(NewNoteController().save(entity))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def save(self, entity: dict):
        item_type = entity['item_type']

        del entity['item_type']

        return Notice(**entity).save() if item_type == TYPE_NOTICE else Note(**entity).save()
