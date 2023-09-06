import re, sys
from datetime import datetime
from constants import TYPE_NOTICE

sys.path.append('../')

STRING_NOTICE_DATE_LENGTH = 16
OFFSET_STRING_NOTICE_DATE_LENGTH = STRING_NOTICE_DATE_LENGTH + 1
ERROR_EMPTY_MESSAGE = 'Empty message'
ERROR_INVALID_DATETIME = 'Invalid datetime'


class NoteMessageParserService():
    def get_entity(self, item: dict) -> dict:
        if not item['message']:
            return {'error': ERROR_EMPTY_MESSAGE}

        item_type = self.get_item_type(item['message'])
        text = self.get_text(item['message'], item_type)

        if not text:
            return {'error': ERROR_EMPTY_MESSAGE}

        entity = {'text': text, 'item_type': item_type}

        if item_type == TYPE_NOTICE:
            try:
                entity['datetime'] = self.get_notice_datetime(item['message'])
            except:
                return {'error': ERROR_INVALID_DATETIME}

        return entity

    def get_item_type(self, text: str) -> str:
        if re.compile("^\d{1,2}.\d{2}.\d{4}\s\d{2}:\d{2}").search(text):
            return 'notice'

        return 'note'

    def get_text(self, message: str, type: str) -> str:
        text = message.strip()

        if type == 'notice':
            text = message[OFFSET_STRING_NOTICE_DATE_LENGTH:].strip()

        return text

    def get_notice_datetime(self, message: str) -> datetime:
        date_string = message[:STRING_NOTICE_DATE_LENGTH]

        return datetime.strptime(date_string, "%d.%m.%Y %H:%M")
