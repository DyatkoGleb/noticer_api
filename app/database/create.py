from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = "mysql+mysqlconnector://" + os.getenv('MYSQL_USER') + ":" + os.getenv('MYSQL_PASSWORD') + "@mysql/" + os.getenv('MYSQL_DATABASE')
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Notices(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)
    datetime = Column(DateTime)

class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)

class Database():
    def __init__(self):
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    def add_new_item(self, db_item: Notes | Notices) -> dict:
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        self.db.close()

        return self.sqlalchemy_object_to_dict(db_item)

    def sqlalchemy_object_to_dict(self, object: Notes | Notices) -> dict:
        return {column.name: getattr(object, column.name) for column in object.__table__.columns}