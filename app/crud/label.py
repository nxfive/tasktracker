# from app.schemas.label import LabelCreate, LabelUpdate
# from app.models.label import DbLabel
# from sqlalchemy.orm import Session
# from app.crud.base import CrudBase
#
#
# class CrudLabel(CrudBase[DbLabel]):
#
#     def create(self, db: Session, request: LabelCreate, *, user_id: int):
#         new_label = self.model(
#             name=request.name,
#             description=request.description,
#             color=request.color,
#             creator_id=user_id
#         )
#         db.add(new_label)
#         db.commit()
#         db.refresh(new_label)
#         return new_label
#
#     def update(self, db: Session, request: LabelUpdate, *, user_id: int, label_id: int):
#         label = db.query(self.model).filter_by(id=label_id).first()
#         if label.creator_id == user_id:
#             data = request.dict(exclude_unset=True)
#             for key, value in data.items():
#                 setattr(label, key, value)
#             db.commit()
#             db.refresh(label)
#             return label
#
#
# crud_label = CrudLabel(DbLabel)
