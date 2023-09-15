import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from services import ModelService
from database import DatabaseSession

sys.path.append('../')
Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)

    db = DatabaseSession().get_session()

    def save(self) -> dict:
        self.db.add(self)
        self.db.commit()
        self.db.refresh(self)
        self.db.close()

        return ModelService().sqlalchemy_object_to_dict(self)

    def create_table(self):
        Note.metadata.create_all(DatabaseSession().engine)