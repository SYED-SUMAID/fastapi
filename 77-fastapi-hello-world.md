# FastAPI Introduction

## 1. What Is FastAPI?

FastAPI is a Python framework used to build APIs. It allows applications to communicate and exchange data through HTTP requests and responses.

It is commonly used to build backend services for websites, mobile applications, and other software.

## 2. Installing FastAPI

Install FastAPI and its standard dependencies using pip:

    pip install "fastapi[standard]"

## 3. Creating Your First API

Create a file named `main.py`.

### Code

    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def home():
        return {"message": "Hello World"}

### Explanation

- `from fastapi import FastAPI` imports the FastAPI class.
- `app = FastAPI()` creates the application.
- `@app.get("/")` defines a GET endpoint for the root URL.
- `def home()` is the function that handles requests to this endpoint.
- `return` sends a JSON response to the client.

### Output

    {
        "message": "Hello World"
        "status": "success"
    }

## 4. Running the Application

Run the application using Uvicorn:

    uvicorn main:app --reload

- `uvicorn` starts the development server.
- `main` refers to the `main.py` file.
- `app` refers to the FastAPI application object.
- `--reload` automatically restarts the server when you change your code.

Open the application at:

    http://127.0.0.1:8000

![alt text](<Screenshot From 2026-10-20 11-33-39.png>)

## 5. Routes and Endpoints

A route defines the URL and HTTP method used to access a particular function.

An endpoint is a specific API address where a client can send a request.

### Example

    @app.get("/users")
    def get_users():
        return {"message": "All users"}

Here, `/users` is the endpoint, and `GET` is the HTTP method.

## 6. HTTP Methods

HTTP methods tell the API what action the client wants to perform.

| Method | Purpose |
|---|---|
| GET | Retrieve data |
| POST | Create data |
| PUT | Update existing data |
| PATCH | Partially update data |
| DELETE | Delete data |

### Example

    @app.get("/")
    def home():
        return {"message": "Welcome"}

The `GET` method is used here to retrieve a response from the API.

## 7. Path Parameters

Path parameters allow us to pass values directly through a URL.

### Code

    @app.get("/users/{user_id}")
    def get_user(user_id: int):
        return {"user_id": user_id}

### Example URL

    http://127.0.0.1:8000/users/10

![alt text](<Screenshot From 2026-10-20 12-11-53.png>)

### Output

    {
        "user_id": 10
    }

### Explanation

- `{user_id}` is a dynamic part of the URL.
- `user_id: int` tells FastAPI that the value should be an integer.
- FastAPI extracts the value from the URL and passes it to the function.

## 8. Query Parameters

Query parameters pass additional information through the URL, usually after a `?` symbol.

### Code

    @app.get("/products")
    def get_products(category: str):
        return {"category": category}

### Example URL

    http://127.0.0.1:8000/products?category=electronics

![alt text](<Screenshot From 2026-10-20 14-33-54.png>)

### Output

    {
        "category": "electronics"
    }

### Explanation

- `category` is a query parameter.
- `?category=electronics` passes the value `electronics`.
- FastAPI receives the value and passes it to the function.

## 9. Automatic API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, open:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

These pages allow you to explore your endpoints and test API requests directly in your browser.

## 10. Important Terms

| Term | Meaning |
|---|---|
| API | Allows different applications to communicate |
| FastAPI | Python framework for building APIs |
| Endpoint | An API address that handles requests |
| Route | Connects a URL and HTTP method to a function |
| HTTP | Protocol used for communication between clients and servers |
| Request | Data or instructions sent to the server |
| Response | Data returned by the server |
| JSON | A common format for exchanging data |
| Uvicorn | Server used to run the FastAPI application |

## 11. Key Takeaway

FastAPI allows us to build APIs using Python functions and decorators. We define endpoints, receive requests, process data, and return responses.

As we progress, we can use path parameters, query parameters, request bodies, Pydantic models, and databases to build complete backend applications.

**Reference:** [Official FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/first-steps/)