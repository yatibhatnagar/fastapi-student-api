from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home
@app.get("/")
def home():
    return {"message": "Student API Running 🚀"}

# CREATE
@app.post("/students")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# READ ALL
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# READ ONE
@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        return {"error": "Student not found"}
    return student

# UPDATE
@app.put("/students/{student_id}")
def update_student(student_id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    student.name = updated.name
    student.age = updated.age
    student.course = updated.course

    db.commit()
    return {"message": "Student updated"}

# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}