import sys
from fastapi import Request
from constants import TYPE_NOTICE
from models.note import Note
from models.notice import Notice
from services.note_message_parser_service import NoteMessageParserService
from response.error_response import ErrorResponse
from response.success_response import SuccessResponse
from database.database_session import DatabaseSession

sys.path.append('../')

FIRST_PAGE_NUMBER = 1
PAGE_SIZE = 20


class NoteController:
    def save_note_action(self, note: dict) -> SuccessResponse | ErrorResponse:
        entity = NoteMessageParserService().get_entity(note)

        if 'error' in entity:
            return ErrorResponse(entity['error']).get()

        try:
            return SuccessResponse(NoteController().save(entity))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def get_notes_action(self, request: Request):
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)

        items = DatabaseSession().get_session().query(Note).offset(offset).limit(page_size).all()

        return SuccessResponse(items)

    def get_notices_action(self, request: Request):
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)

        items = DatabaseSession().get_session().query(Notice).offset(offset).limit(page_size).all()

        return SuccessResponse(items)

    def save(self, entity: dict):
        item_type = entity['item_type']

        del entity['item_type']

        return Notice(**entity).save() if item_type == TYPE_NOTICE else Note(**entity).save()
