from fastapi import  FastAPI
from Users.Users import Participant

app = FastAPI()
 
@app.get("/")
def hello():
    return {"Hello": "World.."}   