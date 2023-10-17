import sys
from fastapi import Request
from constants import TYPE_NOTICE
from models import Note, Notice
from services import NoteMessageParserService
from response import SuccessResponse, ErrorResponse
from database import DatabaseSession
from datetime import datetime
from utils import utils

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

    def delete_note_action(self, note: dict) -> SuccessResponse | ErrorResponse:
        try:
            return SuccessResponse(Note().delete(note))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def delete_notice_action(self, note: dict) -> SuccessResponse | ErrorResponse:
        try:
            return SuccessResponse(Notice().delete(note))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def get_notes_action(self, request: Request):
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)

        items = DatabaseSession().get_session().query(Note).offset(offset).limit(page_size).all()

        return SuccessResponse(items)

    def get_all_notices_action(self, request: Request) -> SuccessResponse:
        return SuccessResponse(self.get_noices(request))

    def get_current_notices_action(self, request: Request) -> SuccessResponse:
        return SuccessResponse(self.get_noices(request, Notice.datetime > datetime.utcnow()))

    def get_noices(self, request: Request, filter = True) -> dict:
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)

        items = (DatabaseSession().get_session().query(Notice)
                 .filter(filter)
                 .offset(offset)
                 .limit(page_size)
                 .all()
                 )
        items = utils.date_formatter(items)

        return items

    def save(self, entity: dict) -> dict:
        item_type = entity['item_type']

        del entity['item_type']

        if item_type == TYPE_NOTICE:
            entity = Notice(**entity).save()
        else:
            entity = Note(**entity).save()

        entity['item_type'] = item_type

        return entity