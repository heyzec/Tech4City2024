from uuid import uuid4
import os
from fastapi.staticfiles import StaticFiles
import base64
from fastapi import FastAPI, Depends, Form, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from model import Model
from fastapi.middleware.cors import CORSMiddleware

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
model = Model("./models/best_11_Jul.pt")


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

# Directory to save uploaded files
UPLOAD_DIRECTORY = "./uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)        

app.mount("/files", StaticFiles(directory=UPLOAD_DIRECTORY), name="files")

@app.post("/analyze/", response_model=PhotoResponse)
async def create_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the uploaded file
    file_extension = os.path.splitext(file.filename)[-1]
    db_input_file_name = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, db_input_file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    file_url = f"/files/{db_input_file_name}"

    # Convert the saved file to base64
    with open(file_path, "rb") as image_file:
        base64_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Predict using the model
    result = model.predict(base64_data)
    db_output_file_name = f"{uuid4()}{file_extension}"
    result_url = os.path.join(UPLOAD_DIRECTORY, db_output_file_name)
    Model.save_base64_to_image(result, result_url)

    db_photo = Photo(url=file_url, predicted_url=result_url)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return PhotoResponse(id=db_photo.id, input=file_url, output=result_url)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
