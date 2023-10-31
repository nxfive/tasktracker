from sqlalchemy.orm import Session
from app.schemas import TaskUpdate, TaskCreate
from app.models.task import DbTask
from typing import Optional
from typing import List, Dict


class CrudTask:
    def __init__(self):
        self.model = DbTask

    def get_all(self, db: Session, *, user_id: int) -> List[DbTask]:
        return db.query(self.model).filter_by(user_id=user_id).all()

    def get_by_id(self, db: Session, *, task_id: int) -> DbTask:
        return db.query(self.model).filter_by(id=task_id).first()

    def create(self, db: Session, request: TaskCreate, *, user_id: int) -> DbTask:
        new_task = self.model(
            title=request.title,
            description=request.description,
            status=request.status,
            priority=request.priority,
            user_id=user_id,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    def update(
        self, db: Session, request: TaskUpdate, *, task_id: int, user_id: int
    ) -> DbTask:
        task = db.query(self.model).filter_by(id=task_id).first()
        if task.user_id == user_id:
            request_data = request.dict(exclude_unset=True)
            for key, value in request_data.items():
                if value is not None:
                    setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task

    def delete(
        self,
        db: Session,
        task: Optional[DbTask] = None,
        *,
        task_id: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, str]:
        # only owner can delete his own group
        if not (task or task_id and user_id):
            return {"error": "Not enough data to process"}
        elif task:
            db.delete(task)
            db.commit()
        else:
            task = db.query(self.model).filter_by(id=task_id).first()
            if task.user_id == user_id:
                db.delete(task)
                db.commit()
        return {"message": "task deleted"}


crud_task = CrudTask()
