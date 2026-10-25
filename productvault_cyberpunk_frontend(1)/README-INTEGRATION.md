# ProductVault Cyberpunk Frontend

This frontend uses your existing FastAPI endpoints and SQLite database.

## 1. Copy files
Copy `templates/` and `static/` into the same directory as your existing `main.py`. Do not replace your existing `main.py` or `products.db`.

## 2. Add the dashboard route to `main.py`
You already have `Request`, `HTMLResponse`, and `Jinja2Templates` imports and a `templates = Jinja2Templates(directory="templates")` line. Add this route after the templates line:

```python
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
```

## 3. Run FastAPI
From the folder containing `main.py`:

```bash
uvicorn main:app --reload
```

If your file is not named `main.py`, replace `main` with the filename (without `.py`).

## 4. Open the dashboard
Go to `http://127.0.0.1:8000/dashboard`.

Swagger remains at `http://127.0.0.1:8000/docs`.

## Expected existing endpoints
- `GET /products`
- `POST /product`
- `PUT /product/{product_id}`
- `DELETE /product/{product_id}`

The UI expects product JSON fields named `product_id`, `name`, `description`, `price`, and `quantity`, matching the SQLModel shown in your existing code.

## Notes
- Product statistics are calculated from the returned database records in the browser.
- Low stock is defined here as quantity <= 5.
- The page uses Google Fonts if internet access is available; the interface still works without it.
