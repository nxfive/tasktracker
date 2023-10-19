from models.task import DbTask
from schemas.task import TaskUpdate, TaskCreate
from sqlalchemy.orm import Session


class CrudTask:

    def __init__(self):
        self.model = DbTask

    def get_all_tasks(self, db: Session, *, user_id: int):
        return db.query(self.model).filter_by(user_id=user_id).all()

    def create_task(self, db: Session, request: TaskCreate, *, user_id: int):
        new_task = self.model(
            title=request.title,
            description=request.description,
            status=request.status,
            priority=request.priority,
            user_id=user_id
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    def update_task(self, db: Session, request: TaskUpdate, *, task_id: int, user_id: int):
        task = db.query(self.model).filter_by(id=task_id).first()
        if task.user_id == user_id:
            request_data = request.dict(exclude_unset=True)
            for key, value in request_data.items():
                if value is not None:
                    setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, *, task_id: int, user_id: int):
        task = db.query(self.model).filter_by(id=task_id).first()
        if user_id == task.user_id:
            db.delete(task)
            db.commit()
        return {"message": "task deleted"}


crud_task = CrudTask()
