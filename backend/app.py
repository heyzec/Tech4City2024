import base64
from fastapi import FastAPI, Depends, Form, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String)
    url = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class PhotoCreate(BaseModel):
    name: str

class PhotoResponse(BaseModel):
    id: int
    name: str
    email: str
    base64_data: str

    class Config:
        from_attributes = True

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/photos/", response_model=PhotoResponse)
async def create_photo(name: str = Form(...), email: EmailStr = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate email format
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    # Read the file and convert it to base64
    file_contents = await file.read()
    base64_data = base64.b64encode(file_contents).decode('utf-8')
    db_photo = Photo(name=name, email=email, url=base64_data)
    print(db_photo)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return PhotoResponse(id=db_photo.id, name=db_photo.name, email=db_photo.email, base64_data=db_photo.url)

@app.get("/photos/", response_model=List[PhotoResponse])
def read_photos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    photos = db.query(Photo).offset(skip).limit(limit).all()
    return [PhotoResponse(id=photo.id, name=photo.name, email=photo.email, base64_data=photo.url) for photo in photos]

@app.get("/photos/{photo_id}", response_model=PhotoResponse)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return PhotoResponse(id=photo.id, name=photo.name, email=photo.email, base64_data=photo.url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
