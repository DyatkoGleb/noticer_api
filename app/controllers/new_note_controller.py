import sys
from constants import TYPE_NOTICE
from models.note import Note
from models.notice import Notice

sys.path.append('../')


class NewNoteController:
    def save_item_action(self, entity: dict) -> dict:
        item_type = entity['item_type']

        del entity['item_type']

        return Notice(**entity).save() if item_type == TYPE_NOTICE else Note(**entity).save()