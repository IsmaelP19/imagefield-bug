from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from .facilities import Facilities 
from core.schemas import schemas


def get_inst(db: Session, inst_id: int):
    return db.query(Facilities).filter(Facilities.ins_fea_id == inst_id).first()


def get_insts(db: Session):
        return db.query(Facilities).all()


def create_inst(db: Session, inst: schemas.InstCreate):
    Facilities = Facilities(**inst.dict())
    db.add(Facilities)
    db.commit()


def update_inst(db: Session, inst_id: int, new_inst: schemas.InstCreate):
    insts = db.query(Facilities).filter(Facilities.ins_fea_id == inst_id).first()
    if insts:
        insts.update(ins_fea_id=inst_id, **new_inst.dict())
        db.commit()
        return insts
    else: 
        raise HTTPException(status_code=404, detail="Facility not found")
