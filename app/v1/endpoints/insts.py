from core.models.facilities_crud import *
from core.schemas import schemas
from fastapi import APIRouter
from sqlalchemy.orm import Session
from dependencies import *
# from users.models import User
from typing import List

router_insts = APIRouter(
    prefix='',
    tags=['facilities']
)

### DATOS DE LAS INTALACIONES ###
@router_insts.get("/insts/{inst_id}", response_model=schemas.InstBase)
def read_inst(inst_id: int, db: Session = Depends(get_db)):
    
    inst = get_inst(db, inst_id=inst_id)
    if inst is None:
        raise HTTPException(status_code=404, detail="Facility not found")

@router_insts.get("/insts", summary='Get all the facilities', response_model=List[schemas.InstBase])
def read_inst(db: Session = Depends(get_db)):
    insts = get_insts(db)
    if insts is None:
        raise HTTPException(status_code=404, detail="No facilities found")
    return insts

@router_insts.post("/insts", response_model=schemas.InstCreate)
async def post_inst(inst: schemas.InstCreate, db: Session = Depends(get_db)):
    create_inst(db, inst)
    return inst

@router_insts.put("/insts/{inst_id}", response_model=schemas.InstCreate)
def put_inst(inst_id: int, inst: schemas.InstCreate, db: Session = Depends(get_db)):
    out = update_inst(db, inst_id, inst)
    return out
