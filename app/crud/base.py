from typing import Generic, TypeVar, Type, List, Union
from app.database.setup import Base
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


class CrudBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(
        self, db: Session, attr_name: str | None = None, id: int | None = None
    ) -> List[ModelType]:
        if id and attr_name:
            # condition = {attribute: value}
            condition = {str(getattr(self.model, attr_name, "")).split(".")[1]: id}
            if "" not in condition:
                return db.query(self.model).filter_by(**condition).all()
        else:
            return db.query(self.model).all()

    def get_by_id(self, db: Session, *, id: int) -> ModelType | None:
        return db.query(self.model).filter_by(id=id).first()

    def get_by_attr(
        self, db: Session, *, attr_name: str, value: Union[str, int]
    ) -> ModelType | None:
        condition = {str(getattr(self.model, attr_name, "")).split(".")[1]: value}
        if "" not in condition:
            return db.query(self.model).filter_by(**condition).first()
