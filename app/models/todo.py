import sys
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from services import ModelService
from database import DatabaseSession

sys.path.append('../')
Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)
    is_completed = Column(Boolean)

    db = DatabaseSession().get_session()

    def create_table(self):
        Todo.metadata.create_all(DatabaseSession().engine)

    def save(self) -> dict:
        self.db.add(self)
        self.db.commit()
        self.db.refresh(self)
        self.db.close()

        return ModelService().sqlalchemy_object_to_dict(self)

    def delete(self, todo: dict) -> dict:
        todo = self.db.query(Todo).filter(Todo.id == todo['todoId']).first()
        self.db.delete(todo)
        self.db.commit()

        return todo
