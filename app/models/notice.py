import sys, os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from services.model_service import ModelService

sys.path.append('../')
load_dotenv()
DATABASE_URL = "mysql+mysqlconnector://" + os.getenv('MYSQL_USER') + ":" + os.getenv('MYSQL_PASSWORD') + "@mysql/" + os.getenv('MYSQL_DATABASE')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()


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