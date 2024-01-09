import sys
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from services import ModelService
from database import DatabaseSession

sys.path.append('../')
Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, index=True)

    ERROR_NOTE_NOT_FOUND = 'Note not found'

    db = DatabaseSession().get_session()

    def create_table(self):
        Note.metadata.create_all(DatabaseSession().engine)

    def save(self) -> dict:
        self.db.add(self)
        self.db.commit()
        self.db.refresh(self)
        self.db.close()

        return ModelService().sqlalchemy_object_to_dict(self)

    def delete(self, note: dict) -> dict:
        note = self.db.query(Note).filter(Note.id == note['id']).first()
        self.db.delete(note)
        self.db.commit()

        return note

    def update(self, updatedNote: dict) -> dict:
        note = self.db.query(Note).filter(Note.id == updatedNote['id']).first()

        if note:
            for key, value in updatedNote.items():
                setattr(note, key, value)
            self.db.commit()

            return ModelService().sqlalchemy_object_to_dict(note)
        else:
            raise Exception(self.ERROR_NOTE_NOT_FOUND)
