import sys
from models.note import Note
from models.notice import Notice
from .database_session import DatabaseSession

sys.path.append('../')


class Database():
    engine = DatabaseSession().get_engine()

    def create_tables(self):
        Note.metadata.create_all(self.engine)
        Notice.metadata.create_all(self.engine)