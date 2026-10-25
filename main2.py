
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field, Session, create_engine, select


# ==========================================
# 1. DATABASE CONFIGURATION
# ==========================================

sqlite_file_name = "products.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False}
)


# ==========================================
# 2. DATABASE MODEL
# ==========================================

class Product(SQLModel, table=True):
    product_id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: int
    quantity: int


# ==========================================
# 3. REQUEST MODELS
# ==========================================

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int = PydanticField(gt=0)
    quantity: int = PydanticField(ge=0)


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = PydanticField(default=None, gt=0)
    quantity: int | None = PydanticField(default=None, ge=0)


# PUT requires all product fields.
class ProductReplace(BaseModel):
    name: str
    description: str
    price: int = PydanticField(gt=0)
    quantity: int = PydanticField(ge=0)


# ==========================================
# 4. DATABASE SESSION
# ==========================================

def get_session():
    with Session(engine) as session:
        yield session


# ==========================================
# 5. CREATE DATABASE TABLES
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")


# ==========================================
# 6. STUDENT MODEL AND ENDPOINT
# ==========================================

class Student(BaseModel):
    name: str
    age: int


@app.post("/students")
def create_student(student: Student):
    return {
        "message": f"Student {student.name} created successfully",
        "age": student.age
    }


# ==========================================
# 7. DASHBOARD
# ==========================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ==========================================
# 8. CREATE A PRODUCT
# ==========================================

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


# ==========================================
# 9. GET ALL PRODUCTS
# ==========================================

@app.get("/products", response_model=list[Product])
def get_all_products(
    session: Session = Depends(get_session)
):
    products = session.exec(select(Product)).all()

    return products


# ==========================================
# 10. GET PRODUCT BY ID
# ==========================================

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


# ==========================================
# 11. UPDATE PRODUCT - PUT
# ==========================================

@app.put("/product/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_data: ProductReplace,
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.quantity = product_data.quantity

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


# ==========================================
# 12. UPDATE SELECTED FIELDS - PATCH
# ==========================================

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


# ==========================================
# 13. DELETE PRODUCT
# ==========================================

@app.delete("/product/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    session.delete(product)
    session.commit()

    return {
        "message": "Product deleted successfully",
        "product_id": product_id
    }

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )