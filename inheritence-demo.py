## blog is child class of Basemodel
## But here Basemodel is our parent class that we created ourself.it is class provided by pydantic..
## by inheriting from it,our Blog gets Pydantics data-validation and data-handling functionality.. 

from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    id:int
    body:str
    published: bool = True

blog = Blog(
    title= "Learning python oop",
    id = 200,
    body = "Fastapi is a python framework"
)

print(blog.title)