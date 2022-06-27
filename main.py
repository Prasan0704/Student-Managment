from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date
from typing import Optional
from app.settings import DATABASE_URL
from app.models import Base, Book



engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def recreate_database():
    Base.metadata.create_all(engine)
recreate_database()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Lets Create Student Management Database"}


@app.post("/students")
async def create_student(Name: str, Regno: int):
    session = Session()
    student = student(
        Name=Name,
        Regno=Regno,
        created_at = date.today()
    )
    session.add(student)
    session.commit()
    session.close()
    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.get("/students/{code}")
async def find_student(Code: int):
    session = Session()
    student = session.query(student).filter(
       student.code == code
    ).first()
    session.close()

    result = jsonable_encoder({
        "student": student
        })
    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
        })


@app.get("/students")
async def get_student(student_count: int = 10, start: int = 1):
    if( student_count > 100 or student_count < 0):
        student_count = 100

    start -= 1
    session = Session()
    students = session.query(student).limit(student_count).offset(start*student_count).all()
    session.close()

    result = jsonable_encoder({
        "students": students
        })

    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
        })


@app.put("/students")
async def update_student(code: int, Name: str = None, Regno: int = None):
    session = Session()
    student = session.query(student).get(code)
    if(Name is not None):
        student.Name = Name
    if(Regno is not None):
        student.Regno = Regno
    session.commit()
    session.close()
    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.delete("/students")
async def delete_book(code: int):
    session = Session()
    student = session.query(student).get(code)
    session.delete(student)
    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "message": message
        })
