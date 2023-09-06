import os, sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from models.note import Note
from models.notice import Notice

sys.path.append('../')
load_dotenv()

DATABASE_URL = "mysql+mysqlconnector://" + os.getenv('MYSQL_USER') + ":" + os.getenv('MYSQL_PASSWORD') + "@mysql/" + os.getenv('MYSQL_DATABASE')
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Database():
    def create_tables(self):
        Note.metadata.create_all(engine)
        Notice.metadata.create_all(engine)