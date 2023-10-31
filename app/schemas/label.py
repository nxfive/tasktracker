# from pydantic import BaseModel
#
#
# class LabelCreate(BaseModel):
#     name: str
#     description: str | None = None
#     color: str | None = "#fff"
#
#
# class LabelUpdate(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     color: str | None = None
#
#
# class LabelDisplay(BaseModel):
#     name: str
#
#     class Config:
#         orm_mode = True
#