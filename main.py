from fastapi import FastAPI
from blog import schemas

app = FastAPI()

@app.get('/blog')
def create(request: schemas.Blog):
    return request