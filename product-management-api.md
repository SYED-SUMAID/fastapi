# Product Management API

A simple REST API built with **FastAPI** and **SQLModel** for managing products, backed by a SQLite database. It includes a dashboard page and auto-generated interactive API docs.

## Features

- Full CRUD operations for products
- Full update (PUT) and partial update (PATCH) support
- Request validation with Pydantic
- SQLite database, created automatically on startup
- Interactive API docs (Swagger UI)
- HTML dashboard served with Jinja2

## Tech Stack

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- Jinja2
- Uvicorn

## Project Structure

- `main.py` - application code
- `templates/index.html` - dashboard template
- `products.db` - SQLite database (auto-generated)

## Installation

1. Clone the repository and open the project folder.
2. Install dependencies: `pip install fastapi uvicorn sqlmodel jinja2`
3. Start the server: `uvicorn main:app --reload`

## API Documentation

Once the server is running, all endpoints can be viewed and tested directly in the browser:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/product` | Create a new product |
| GET | `/products` | Get all products |
| GET | `/product/{product_id}` | Get a product by ID |
| PUT | `/product/{product_id}` | Replace a product (all fields required) |
| PATCH | `/product/{product_id}` | Update selected fields |
| DELETE | `/product/{product_id}` | Delete a product |
| GET | `/dashboard` | Open the dashboard |

## Product Model

| Field | Type | Rules |
|-------|------|-------|
| `product_id` | integer | Auto-generated primary key |
| `name` | string | Required |
| `description` | string | Required |
| `price` | integer | Must be greater than 0 |
| `quantity` | integer | Must be 0 or greater |

## Code Overview

### Database Model

The `Product` table is defined with SQLModel. The primary key is generated automatically by the database.

    class Product(SQLModel, table=True):
        product_id: int | None = Field(default=None, primary_key=True)
        name: str
        description: str
        price: int
        quantity: int

### Request Validation

Incoming data is validated with Pydantic before it reaches the database. Price must be positive and quantity cannot be negative.

    class ProductCreate(BaseModel):
        name: str
        description: str
        price: int = PydanticField(gt=0)
        quantity: int = PydanticField(ge=0)

### Create a Product (POST)

The validated data is converted into a `Product`, saved, and returned with its generated ID.

    @app.post("/product", response_model=Product)
    def add_product(
        product_data: ProductCreate,
        session: Session = Depends(get_session)
    ):
        product = Product(**product_data.model_dump())

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

### Get a Product by ID (GET)

If the product does not exist, the API responds with a 404 error.

    @app.get("/product/{product_id}", response_model=Product)
    def get_product(
        product_id: int,
        session: Session = Depends(get_session)
    ):
        product = session.get(Product, product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product

### Update Selected Fields (PATCH)

Only the fields sent in the request are updated. Fields that are not sent keep their current values.

    @app.patch("/product/{product_id}", response_model=Product)
    def patch_product(
        product_id: int,
        product_data: ProductUpdate,
        session: Session = Depends(get_session)
    ):
        product = session.get(Product, product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

## Error Handling

- `404 Not Found` - returned when a product ID does not exist
- `422 Unprocessable Entity` - returned when request data fails validation

## More Methods

This README shows only a few examples to keep things short. To see the remaining methods (GET all products, PUT, DELETE, and the dashboard route), check the full source code in `main.py` in this repository.

## Screenshots

### API Documentation



### Dashboard

<!-- Add dashboard screenshot here -->