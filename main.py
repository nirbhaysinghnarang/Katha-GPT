from fastapi import FastAPI
from pydantic import BaseModel
from story import Katha

class RequestBody(BaseModel):
   query:str


app = FastAPI()


@app.post("/getstory/")
async def get_story(body: RequestBody):
    katha = Katha(body.query)
    katha.build_story()
    katha.build_pages()
    return katha

