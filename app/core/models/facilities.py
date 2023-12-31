from typing import List
from sqlalchemy import  Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from starlette_admin import BaseModelView
# from starlette_admin.fields import 
from starlette_admin.contrib.sqla import ModelView
from sqlalchemy_file import ImageField
from .database import Base
from .users import User

facilities_user_association = Table(
    "facilities_user_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("facility_id", Integer, ForeignKey("facilities.ins_fea_id")),
)


class Facilities(Base):
    __tablename__ = "facilities"

    ins_fea_id = Column(Integer, primary_key=True)
    ins_fea_name = Column(String, nullable=False)
    ins_fea_desc = Column(String)
    users: Mapped[List[User]] = relationship(secondary=facilities_user_association, back_populates="facilities")
    ins_fea_img = Column(ImageField())
    # ins_fea_img = Column(String)

    async def __admin_repr__(self, request):
        return f"{self.ins_fea_name}"
    
    async def __admin_select2_repr__(self, request):
        return f'<span>#{(self.ins_fea_id)}</span> <strong>{(self.ins_fea_name)}</strong>'
        

    def update(self, ins_fea_id=None, ins_fea_name=None, ins_fea_desc=None, ins_fea_img=None):
        self.ins_fea_id = ins_fea_id
        self.ins_fea_name = ins_fea_name
        self.ins_fea_desc = ins_fea_desc
        self.ins_fea_img = ins_fea_img

class Insts_View(ModelView):
    # exclude_fields_from_list = ['ins_fea_img']
    # exclude_fields_from_detail = ['ins_fea_img']
    fields = ['ins_fea_id', 'ins_fea_name', 'ins_fea_desc', 'ins_fea_img', 'users']
