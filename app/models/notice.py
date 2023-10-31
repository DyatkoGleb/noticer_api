import sys
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from services import ModelService
from database import DatabaseSession

sys.path.append('../')
Base = declarative_base()


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)
    datetime = Column(DateTime)

    db = DatabaseSession().get_session()

    def create_table(self):
        Notice.metadata.create_all(DatabaseSession().engine)

    def save(self) -> dict:
        self.db.add(self)
        self.db.commit()
        self.db.refresh(self)
        self.db.close()

        return ModelService().sqlalchemy_object_to_dict(self)

    def delete(self, notice: dict):
        notice = self.db.query(Notice).filter(Notice.id == notice['id']).first()
        self.db.delete(notice)
        self.db.commit()

        return notice