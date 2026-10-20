from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}



@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# @app.get("/products")
# def get_products(category:str):
#     return {"category": category}


@app.get("/items")
def get_products(category: str):
    return {"category": category}