# FastAPI Basic (Course Project)

Backend Python practice project using:
- FastAPI
- Pydantic & pydantic-settings
- SQLModel
- Alembic
- Scalar (API docs UI)
- SQLite

## Prerequisites

- Python `>=3.14`
- `uv` installed

## Install Dependencies

```bash
uv sync
```

## Run App

```bash
make dev
```

Server default: `http://127.0.0.1:8000`

## API Documentation

- Scalar UI: `http://127.0.0.1:8000/scalar`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Database Configuration

The project uses SQLite with the default URL:

`sqlite:///database.db`

Settings location:
- `/Users/ghiffari/Documents/personal/course/fastapi-basic/app/core/settings.py`

## Alembic Migration

Migration initialization (already set up):
- `/Users/ghiffari/Documents/personal/course/fastapi-basic/alembic`
- `/Users/ghiffari/Documents/personal/course/fastapi-basic/alembic.ini`

Common commands:

```bash
.venv/bin/alembic current
.venv/bin/alembic upgrade head
.venv/bin/alembic downgrade -1
```

## Available Endpoints

Base URL: `http://127.0.0.1:8000`

### 1. `GET /products`

Headers (required):
- `X-Request-ID`: UUID

Query params:
- `limit` (default `10`)
- `offset` (default `0`)

Example:

```bash
curl -X GET "http://127.0.0.1:8000/products?limit=10&offset=0" \
  -H "X-Request-ID: 25769c6c-d34d-4bfe-ba98-e0ee856f3e7a"
```

### 2. `POST /products`

Headers (required):
- `X-Request-ID`: UUID

Body:
- `sku` (integer, min `3`)
- `name` (string, min length `3`)
- `description` (optional string)
- `price` (float, max `999999999.0`)
- `currency` (`USD` or `IDR`)
- `stock` (integer, max `1000`)

Example:

```bash
curl -X POST "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 25769c6c-d34d-4bfe-ba98-e0ee856f3e7a" \
  -d '{
    "sku": 1001,
    "name": "Keyboard Mechanical",
    "description": "Switch brown",
    "price": 750000,
    "currency": "IDR",
    "stock": 20
  }'
```

## Project Structure

```text
app/
  core/
    settings.py
  models/
    database.py
    engine.py
  router/
    product.py
  schema/
    product.py
  utils/
    query_params.py
alembic/
alembic.ini
```

## Notes

- If the `X-Request-ID` header is not provided, request validation will fail.
- SQLAlchemy echo logging is enabled in the engine (`echo=True`) to help with SQL debugging.
