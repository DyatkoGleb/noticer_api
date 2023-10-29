import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


class DatabaseSession:
    _instance = None
    database_url = ("mysql+mysqlconnector://" + os.getenv('MYSQL_USER') + ":" +
        os.getenv('MYSQL_PASSWORD') + "@mysql/" + os.getenv('MYSQL_DATABASE'))
    def __new__(self):
        if self._instance is None:
            self._instance = super(DatabaseSession, self).__new__(self)
            self._instance.engine = create_engine(self.database_url, pool_size=20)

            try:
                self._instance.engine.connect()
            except exc.OperationalError:
                self.create_database()

            self._instance.Session = sessionmaker(bind=self._instance.engine)
        return self._instance

    def create_database(self):
        from sqlalchemy_utils import create_database
        create_database(self.database_url)

    def get_session(self):
        return self.Session()

    def get_engine(self):
        return self.engine