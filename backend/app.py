import base64
from typing import List

from fastapi import FastAPI, Depends, Form, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from model import Model

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
model = Model("./backend/models/best_11_Jul.pt")


origins = [
    "*",
]


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String)
    predicted_url = Column(String)


Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class PhotoResponse(BaseModel):
    id: int
    input: str
    output: str

    class Config:
        from_attributes = True

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/analyze/", response_model=PhotoResponse)
async def create_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the file and convert it to base64
    file_contents = await file.read()
    base64_data = base64.b64encode(file_contents).decode('utf-8')
    result = model.predict(base64_data)

    db_photo = Photo(url=base64_data, predicted_url=result)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return PhotoResponse(id=db_photo.id, input=base64_data, output=result)


@app.get("/results", response_model=List[PhotoResponse])
def read_photos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if limit == -1:
        photos = db.query(Photo).offset(skip).all()
    else:
        photos = db.query(Photo).offset(skip).limit(limit).all()  # Default limit 10
    return [PhotoResponse(id=photo.id, input=photo.url, output=photo.predicted_url) for photo in photos]


@app.get("/results/{photo_id}", response_model=PhotoResponse)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return PhotoResponse(id=photo.id, input=photo.url, output=photo.predicted_url)


@app.delete("/delete")
def delete_all_photos(db: Session = Depends(get_db)):
    try:
        db.query(Photo).delete()
        db.commit()
        return {"message": "All entries deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete entries: {str(e)}")


# Static files
############################################################

@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")

app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")


@app.get("/styles.css")
def read_css():
    return FileResponse("frontend/styles.css")

@app.get("/script.js")
def read_js():
    return FileResponse("frontend/script.js")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
