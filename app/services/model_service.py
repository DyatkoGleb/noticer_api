class ModelService:
    def sqlalchemy_object_to_dict(self, object) -> dict:
        return {column.name: getattr(object, column.name) for column in object.__table__.columns}