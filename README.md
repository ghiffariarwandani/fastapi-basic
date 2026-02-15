# Product & Category Management API

Example FastAPI application for course practice.

This project demonstrates REST API development with FastAPI + SQLModel, including many-to-many relationships between products and categories.

## Features

- Product CRUD (`/products`)
- Category CRUD (`/categories`)
- Many-to-many relation (`product` <-> `category`) via `productcategorylink`
- Pagination support (`limit`, `offset`)
- Request/response validation with Pydantic
- Alembic migration workflow
- Seeder script with realistic coffee equipment dataset
- API docs with Scalar UI

## Tech Stack

- FastAPI
- SQLModel
- SQLite (default)
- Pydantic
- Alembic
- UV
- Ruff

## Prerequisites

- Python `>=3.14`
- `uv` installed

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

### 2. Apply migrations

```bash
.venv/bin/alembic upgrade head
```

### 3. Seed data

```bash
uv run python -m script.seeder
```

### 4. Run app

```bash
make dev
```

Server default: `http://127.0.0.1:8000`

## API Documentation

- Scalar UI: `http://127.0.0.1:8000/scalar`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Request Header Rules

`X-Request-ID` is required for write operations:

- `POST /products`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`
- `POST /categories`
- `PUT /categories/{category_id}`
- `DELETE /categories/{category_id}`

Example header value:

```text
X-Request-ID: 25769c6c-d34d-4bfe-ba98-e0ee856f3e7a
```

## API Endpoints

Base URL: `http://127.0.0.1:8000`

### Products

- `GET /products` - List products (supports `limit`, `offset`)
- `GET /products/{product_id}` - Get product by ID
- `POST /products` - Create product
- `PUT /products/{product_id}` - Partial update product fields
- `DELETE /products/{product_id}` - Delete product

### Categories

- `GET /categories` - List categories (supports `limit`, `offset`)
- `GET /categories/{category_id}` - Get category by ID
- `POST /categories` - Create category
- `PUT /categories/{category_id}` - Partial update category fields
- `DELETE /categories/{category_id}` - Delete category

## Example Usage

### List products

```bash
curl -X GET "http://127.0.0.1:8000/products?limit=10&offset=0"
```

### Create category

```bash
curl -X POST "http://127.0.0.1:8000/categories" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 25769c6c-d34d-4bfe-ba98-e0ee856f3e7a" \
  -d '{
    "name": "Espresso Machine",
    "description": "Machines for making espresso shots"
  }'
```

### Create product

```bash
curl -X POST "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 25769c6c-d34d-4bfe-ba98-e0ee856f3e7a" \
  -d '{
    "sku": 12001,
    "name": "Breville Bambino Plus BES500",
    "description": "Compact espresso machine",
    "price": 10999000,
    "currency": "IDR",
    "stock": 10
  }'
```

### Update product (partial)

```bash
curl -X PUT "http://127.0.0.1:8000/products/<product_id>" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 25769c6c-d34d-4bfe-ba98-e0ee856f3e7a" \
  -d '{
    "name": "Breville Bambino Plus (Updated)",
    "stock": 8
  }'
```

## Response Format

Most list/create/update endpoints return envelope format:

```json
{
  "data": {},
  "message": "Success ..."
}
```

## Database & Migration Notes

Default DB URL is configured in:

- `app/core/settings.py`

Default value:

```text
sqlite:///database.db
```

Useful Alembic commands:

```bash
.venv/bin/alembic current
.venv/bin/alembic upgrade head
.venv/bin/alembic downgrade -1
```

## Project Structure

```text
app/
  main.py
  core/
    settings.py
  models/
    database.py
    engine.py
  router/
    product.py
    category.py
  schema/
    product.py
    category.py
  types/
    enums.py
  utils/
    query_params.py
script/
  seeder.py
alembic/
alembic.ini
makefile
```

## Notes

- Pagination validation:
  - `limit >= 1`
  - `offset >= 0`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
