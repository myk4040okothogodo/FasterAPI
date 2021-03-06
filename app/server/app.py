from fastapi import FastAPI

from  server.routes.student import router as StudentRouter
app = FastAPI()


"""Tags are identifiers used to group routes.Routes with the same tags are grouped into a scetion on the API documentation."""

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
@app.get("/", tags=["Root"]) 
async def read_root():
    return {"message": "Welcome to the funzafunzi app."}
