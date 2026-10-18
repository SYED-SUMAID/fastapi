from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BlogBase(BaseModel):
    title:str
    body:str
    published:bool = True

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int

@app.get("/blogs", response_model=BlogCreate)
def create_blog(blog:BlogCreate):
    saved_blog = {
        "id": 101,
        "title": blog.title,
        "published" : blog.published 
    }    
    return saved_blog