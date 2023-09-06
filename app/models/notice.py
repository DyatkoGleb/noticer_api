import sys
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from services.model_service import ModelService
from database.database_session import DatabaseSession

sys.path.append('../')
Base = declarative_base()
db = DatabaseSession().get_session()


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)
    datetime = Column(DateTime)

    def save(self) -> dict:
        db.add(self)
        db.commit()
        db.refresh(self)
        db.close()

        return ModelService().sqlalchemy_object_to_dict(self)