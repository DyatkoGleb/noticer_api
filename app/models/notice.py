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

    ERROR_NOTICE_NOT_FOUND = 'Notice not found'

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

    def update(self, updatedNotice: dict) -> dict:
        notice = self.db.query(Notice).filter(Notice.id == updatedNotice['id']).first()

        if notice:
            for key, value in updatedNotice.items():
                setattr(notice, key, value)
            self.db.commit()

            return ModelService().sqlalchemy_object_to_dict(notice)
        else:
            raise Exception(self.ERROR_NOTICE_NOT_FOUND)
