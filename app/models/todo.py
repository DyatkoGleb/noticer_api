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
    is_completed = Column(Boolean, default=False)

    ERROR_TODO_NOT_FOUND = 'Todo not found'

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
        todo = self.db.query(Todo).filter(Todo.id == todo['id']).first()
        self.db.delete(todo)
        self.db.commit()

        return todo

    def update(self, updatedTodo: dict) -> dict:
        todo = self.db.query(Todo).filter(Todo.id == updatedTodo['id']).first()

        if todo:
            for key, value in updatedTodo.items():
                setattr(todo, key, value)
            self.db.commit()

            return ModelService().sqlalchemy_object_to_dict(todo)
        else:
            raise Exception(self.ERROR_TODO_NOT_FOUND)
