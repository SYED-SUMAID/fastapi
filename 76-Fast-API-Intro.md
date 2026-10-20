# 76. FastAPI Introduction

## What is an API?

An API (Application Programming Interface) allows two applications to communicate with each other by sending requests and receiving responses.

**Example:** A weather application uses an API to fetch weather data from a server.

## What is FastAPI?

FastAPI is a modern Python web framework used to build APIs quickly and efficiently.

### Key Features
- High performance
- Automatic data validation
- Interactive API documentation
- Asynchronous programming support
- Python type hints

## How FastAPI Works

1. A client sends a request.
2. FastAPI processes the request.
3. A Python function executes.
4. FastAPI returns a response, commonly in JSON format.

## Simple Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

**Output:**

```json
{
    "message": "Hello World"
}
```

## Related Technologies

- **Python:** Programming language
- **Uvicorn:** ASGI server used to run FastAPI
- **HTTP:** Protocol for communication
- **JSON:** Format for exchanging data

## Documentation

[FastAPI Official Documentation](https://fastapi.tiangolo.com/)