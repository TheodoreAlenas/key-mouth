from a_feature import say_hi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/message")
async def root():
    return {"message": say_hi()}

app.mount("/pages",
          StaticFiles(directory="../web_front/.next/server/pages"),
          name="pages")
