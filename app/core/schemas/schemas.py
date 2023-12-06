from pydantic import BaseModel
from typing import Optional

class InstBase(BaseModel):
    ins_fea_name: str
    ins_fea_desc: str
    ins_fea_img: Optional[str] = None
 
    class Config:
        from_attributes = True


class InstCreate(InstBase):
    ins_fea_id: int

