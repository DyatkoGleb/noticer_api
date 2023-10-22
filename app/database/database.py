import sys
sys.path.append('../')


class Database():
    def create_tables(self):
        from models import Note, Todo, Notice

        Note().create_table()
        Todo().create_table()
        Notice().create_table()