import sys
from fastapi import Request
from constants import TYPE_NOTICE, TYPE_NOTE
from models import Note, Todo, Notice
from services import NoteMessageParserService
from response import SuccessResponse, ErrorResponse
from database import DatabaseSession
from services import ModelService
from datetime import datetime, timedelta
from utils import utils

sys.path.append('../')

FIRST_PAGE_NUMBER = 1
PAGE_SIZE = 20


class NoteController:
    def save_note_action(self, note: dict) -> SuccessResponse | ErrorResponse:
        try:
            entity = NoteMessageParserService().get_note_entity(note)

            return SuccessResponse(NoteController().save(entity))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def save_updated_note_action(self, note: dict) -> SuccessResponse | ErrorResponse:
        try:
            return SuccessResponse(NoteController().update(note))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def delete_note_action(self, entity: Note | Todo | Notice, note: dict) -> SuccessResponse | ErrorResponse:
        try:
            return SuccessResponse(entity().delete(note))
        except Exception as e:
            return ErrorResponse(str(e)).get()

    def get_notes_action(self, request: Request):
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)

        items = DatabaseSession().get_session().query(Note).offset(offset).limit(page_size).all()

        return SuccessResponse(items)

    def get_todos_action(self, request: Request):
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)

        items = DatabaseSession().get_session().query(Todo).offset(offset).limit(page_size).all()

        return SuccessResponse(items)

    def get_all_notices_action(self, request: Request) -> SuccessResponse:
        return SuccessResponse(self.get_notices(request))

    def get_current_notices_action(self, request: Request) -> SuccessResponse:
        return SuccessResponse(self.get_notices(request, Notice.datetime > datetime.utcnow()))

    def get_notes_for_next_day(self, request: Request) -> SuccessResponse:
        next_day = datetime.utcnow() + timedelta(days=1)
        filter_condition = (Notice.datetime >= next_day) & (Notice.datetime < next_day + timedelta(days=1))

        return SuccessResponse(self.get_notices(request, filter_condition))

    def get_notices(self, request: Request, filter = True) -> dict:
        params = dict(request.query_params)
        page_size = abs(int(params.get('pageSize', PAGE_SIZE)))
        page = abs(int(params.get('page', FIRST_PAGE_NUMBER)))
        offset = (int(page) - 1) * int(page_size)
        now = datetime.now()

        notices = (DatabaseSession().get_session().query(Notice)
            .filter(filter)
            .offset(offset)
            .limit(page_size)
            .all()
        )

        for i in range(len(notices)):
            notices[i] = ModelService().sqlalchemy_object_to_dict(notices[i])
            notices[i]['status'] = 'past' if now > notices[i]['datetime'] else 'future'
            notices[i]['true_datetime'] = notices[i]['datetime']

        notices = sorted(notices, key=lambda x: x['datetime'])

        notices = utils.date_formatter(notices)

        return notices

    def save(self, entity: dict) -> dict:
        item_type = entity['item_type']

        del entity['item_type']

        if item_type == TYPE_NOTICE:
            entity = Notice(**entity).save()
            entity = utils.date_formatter([entity])[0]
        elif item_type == TYPE_NOTE:
            entity = Note(**entity).save()
        else:
            entity = Todo(**entity).save()

        entity['item_type'] = item_type

        return entity

    def update(self, entity: dict) -> dict:
        item_type = entity['itemType']

        del entity['itemType']

        if item_type == TYPE_NOTICE:
            notice_datetime = entity['datetime']
            notice_datetime = datetime.strptime(notice_datetime, "%d.%m.%Y %H:%M")
            entity['datetime'] = notice_datetime
            entity = Notice().update(entity)
            entity = utils.date_formatter([entity])[0]
        elif item_type == TYPE_NOTE:
            entity = Note().update(entity)
        else:
            entity = Todo().update(entity)

        return entity