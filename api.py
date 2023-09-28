from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from story_retriever import StoryRetriever
from story_config import StoryConfig
from story import Story
from story_config import ImageGenStyle



class RequestBody(BaseModel):
   query:str
   age:str
   language:str
   imageGenStyle:str
   color:str

app = FastAPI()
@app.post("/getstory/")
async def get_story(body: RequestBody):
	if body.age not in ["preteen", "teen", "adult"]:
		raise HTTPException(404)
	if body.imageGenStyle not in ["Hyperrealistic", "Comic", "Black and White", "Watercolor"]:
		raise HTTPException(404)
	if body.language not in ["english"]:
		raise HTTPException(404)
	if body.color not in ["Color", "Black and White"]:
		raise HTTPException(404)

	most_relevant_content = StoryRetriever(body.query).retrieve()
	config = StoryConfig(
		body.age,
		body.language, 
		most_relevant_content, 
		body.imageGenStyle,
		body.color
	)
	story = Story(config=config)
	story.build_story()
	story.build_pages()
	return story


