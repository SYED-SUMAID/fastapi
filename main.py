from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up the templates directory
templates = Jinja2Templates(directory="templates")


# 1. Root endpoint: Returns JSON
@app.get("/")
def read_root():
    return {
        "message": "Hello World",
        "status": "success"
    }



# 2. Path and query parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "query": q
    }


# 3. Request information
@app.get("/info")
def get_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path
    }

# 4. Read query parameters from the Request object
@app.get("/search")
def search_items(request: Request):
    return {
        "query": request.query_params.get("q")
    }

# 5. Read request headers
@app.get("/browser")
def get_browser(request: Request):
    return {
        "user_agent": request.headers.get("user-agent")
    }

# 6. Read path parameters and query parameters together
@app.get("/users/{user_id}")
def get_user(user_id: int, request: Request):
    return {
        "user_id": user_id,
        "name": request.query_params.get("name")
    }


# 7. Render an HTML page using Jinja2
@app.get("/web", response_class=HTMLResponse)
def read_web_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": "Sumaid",
            "message": "This page is served dynamically using Jinja2!"
        }
    )

class Student(BaseModel):
    name: str
    age: int


@app.post("/students")
def create_student(student: Student):
    return {
        "message": f"Student {student.name} created successfully",
        "age": student.age
    }



# class Blog(BaseModel):
#   title: str
#   body: str
#   id: int
#   published: Optional[bool] = True



# @app.post("/blog")
# def create_blog(
#     title: str = Body(...),
#     body: str = Body(...),
#     id: int = Body(...),
#     published: bool = Body(True),
# ):
#     return {
#         "message": "Saved!",
#         "blog": {
#             "title": title,
#             "body": body,
#             "id": id,
#             "published": published,
#         },
#     }

class Product(BaseModel):
    name:str
    description:str
    price:int
    quantity:int

products = [
    {
        "product_id": 1,
        "name": "Smartphone",
        "description": "A smartphone with 128GB storage and a high-quality camera.",
        "price": 700,
        "quantity": 15
    },
    {
        "product_id": 2,
        "name": "Laptop",
        "description": "A laptop with 16GB RAM and 512GB SSD storage.",
        "price": 1200,
        "quantity": 10
    },
    {
        "product_id": 3,
        "name": "Pen",
        "description": "A smooth-writing blue ink ballpoint pen.",
        "price": 2,
        "quantity": 100
    },
    {
        "product_id": 4,
        "name": "Table",
        "description": "A wooden study table suitable for home or office use.",
        "price": 150,
        "quantity": 8
    }
]

@app.get("/products")
def get_all_prod():
    return products


@app.get("/product/{ID}")
def get_prod_by_id(ID:int):

    for product in products:
        if product["product_id"] == ID:
            return product
        
    return "product not found"

@app.post("/product")
def add_prod(prod: dict = Body(...)):
    products.append(prod)
    return prod

@app.put ("/product/{id}")
def update_cart(id:int,product:Product):
    for p in products:
        if p["product_id"] == id:
            p.update(product.model_dump())
            return{
                "message": "product update successfully",
                "product": p
            }

    return {"message": "product not found"}     


@app.delete("/product/{id}")
def delete_product(id:int):
    for p in products:
        if p["product_id"] == id:
            products.remove(p)
            return {
                "message": "product deleted successfully",
                "product": p
