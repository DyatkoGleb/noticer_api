import sys
from database import create as createDB
from constants import TYPE_NOTICE

sys.path.append('../')


class NewNoteController:
    def save_item_action(self, entity: dict) -> dict:
        return createDB.Database().add_new_item(self.make_new_db_item(entity))

    def make_new_db_item(self, entity: dict) -> createDB.Note | createDB.Notice:
        item_type = entity['item_type']

        del entity['item_type']

        return createDB.Notice(**entity) if item_type == TYPE_NOTICE else createDB.Note(**entity)