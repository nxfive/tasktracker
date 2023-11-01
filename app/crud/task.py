from app.models.task import DbTask
from app.schemas.task import TaskUpdate, TaskCreate
from sqlalchemy.orm import Session
from app.crud.base import CrudBase


class CrudTask(CrudBase[DbTask]):
    def create(self, db: Session, request: TaskCreate, *, user_id: int):
        new_task = self.model(**request.dict(exclude={"model_config"}), user_id=user_id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    def update(self, db: Session, request: TaskUpdate, *, task_id: int, user_id: int):
        task = db.query(self.model).filter_by(id=task_id).first()
        if task.user_id == user_id:
            request_data = request.dict(exclude_unset=True)
            for key, value in request_data.items():
                if value is not None:
                    setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db: Session, *, task_id: int, user_id: int):
        task = db.query(self.model).filter_by(id=task_id).first()
        if user_id == task.user_id:
            db.delete(task)
            db.commit()
        return {"message": "task deleted"}


crud_task = CrudTask(DbTask)
