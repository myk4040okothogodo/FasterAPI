from decouple import config
from bson.objectid import ObjectId
import motor.motor_asyncio

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")


#a serializing callback function

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study":student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
        }


#the following functions will produce concurrent objects(yield and resume structure)
#retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

#Add a new student into the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)

#retrieve a student with matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)

#Update a student with a matching ID
async def update_student(id:str, data:dict):
    #return false if an empty request body is sent
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"id": ObjectId(id)}, {"$set": data}
            )
        if updated_student:
            return True
        return False

#Delete a student from the database
async def delete_student(id:str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": objectId(id)})
        return True
        

















