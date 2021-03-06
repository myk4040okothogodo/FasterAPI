from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
    )

from server.models.student import (

    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
    )

router = APIRouter()

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")

@router.get("/", response_description="students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")

@router.get("/{id}", response_description="student data retrieved")
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorReponseModel("An error occurrred.", 404, "student doesnt exist")


@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            "student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
            )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
        )

@router.delete("/{id}",response_description="Student data deleted from the database")
async def delete_student_data(id:str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
            )
    return ErrorResponseModel(
             "An error occured", 404, "Student with id {0} doesnt exist".format(id)
        )





    
