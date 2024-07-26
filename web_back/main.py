from a_feature import say_hi
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": say_hi()}
