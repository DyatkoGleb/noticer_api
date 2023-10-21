import re, sys
from datetime import datetime
from constants import TYPE_NOTICE

sys.path.append('../')


class NoteMessageParserService():
    STRING_NOTICE_DATE_LENGTH = 16
    OFFSET_STRING_NOTICE_DATE_LENGTH = STRING_NOTICE_DATE_LENGTH + 1
    ERROR_EMPTY_MESSAGE = 'Empty message'
    ERROR_INVALID_DATETIME = 'Invalid datetime'

    def get_note_entity(self, item: dict) -> dict:
        if not item['message']:
            raise Exception(self.ERROR_EMPTY_MESSAGE)

        entity = {'item_type': self.get_item_type(item)}

        if entity['item_type'] == TYPE_NOTICE:
            entity['datetime'] = self.get_datetime(item)

        entity['text'] = self.get_text(item, entity)

        return entity

    def get_item_type(self, item: dict) -> str:
        if 'itemType' in item:
            return item['itemType']

        if re.compile("^\d{1,2}.\d{2}.\d{4}\s\d{2}:\d{2}").search(item['message']):
            return 'notice'

        return 'note'

    def get_datetime(self, item: dict) -> datetime:
        if 'datetime' in item:
            return datetime.strptime(item['datetime'], "%d.%m.%Y %H:%M")

        return self.get_notice_datetime(item['message'])

    def get_text(self, item: dict, entity: dict) -> str:
        text = item['message'].strip()

        if entity['item_type'] == 'notice' and not 'datetime' in item:
            text = text[self.OFFSET_STRING_NOTICE_DATE_LENGTH:].strip()

        if not text:
            raise Exception(self.ERROR_EMPTY_MESSAGE)

        return text

    def get_notice_datetime(self, message: str) -> datetime:
        date_string = message[:self.STRING_NOTICE_DATE_LENGTH]

        notice_datetime = datetime.strptime(date_string, "%d.%m.%Y %H:%M")
        now = datetime.now()

        if notice_datetime < now:
            raise Exception(self.ERROR_INVALID_DATETIME)

        return notice_datetime
