from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from databases import Database
from models import Base, Member as MemberModel
from schemas import Member, MemberCreate
from database import database, engine, SessionLocal

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# Pagination class
class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/members/", response_model=Member)
async def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = MemberModel(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.get("/members/", response_model=List[Member])
async def get_members(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search by name or telegram_id"),
    min_age: Optional[int] = Query(None, ge=0),
    max_age: Optional[int] = Query(None),
    sex: Optional[str] = Query(None, regex="^(ذكر|انثى)$")
):
    query = db.query(MemberModel)
    
    # Search functionality
    if search:
        query = query.filter(
            (MemberModel.name.contains(search)) |
            (MemberModel.telegram_id.contains(search))
        )
    
    # Filtering
    if min_age is not None:
        query = query.filter(MemberModel.age >= min_age)
    if max_age is not None:
        query = query.filter(MemberModel.age <= max_age)
    if sex:
        query = query.filter(MemberModel.sex == sex)
    
    # Pagination
    total = query.count()
    members = query.offset(pagination.skip).limit(pagination.limit).all()
    
    return members

@app.get("/members/{member_id}", response_model=Member)
async def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.put("/members/{member_id}", response_model=Member)
async def update_member(member_id: int, member: MemberCreate, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    for key, value in member.dict().items():
        setattr(db_member, key, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member

@app.delete("/members/{member_id}")
async def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(db_member)
    db.commit()
    return {"message": "Member deleted"}