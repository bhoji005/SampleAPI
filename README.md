# SampleAPI

A sample REST API in Python (FastAPI) demonstrating CRUD operations on an `items` resource,
backed by a thread-safe in-memory store, with a pytest test suite.

## Endpoints

| Method | Path          | Description                        | Success |
| ------ | ------------- | ---------------------------------- | ------- |
| GET    | `/health`     | Health check                       | 200     |
| GET    | `/items`      | List items (`skip`, `limit` query) | 200     |
| POST   | `/items`      | Create an item                     | 201     |
| GET    | `/items/{id}` | Fetch one item                     | 200     |
| PUT    | `/items/{id}` | Replace an item                    | 200     |
| PATCH  | `/items/{id}` | Partially update an item           | 200     |
| DELETE | `/items/{id}` | Delete an item                     | 204     |

Unknown ids return `404`; invalid payloads return `422`.

Interactive docs are served at `/docs` (Swagger UI) and `/redoc`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Example:

```bash
curl -X POST localhost:8000/items -H 'Content-Type: application/json' \
  -d '{"name": "Widget", "description": "A useful widget", "price": 9.99, "quantity": 3}'
curl localhost:8000/items
curl -X PATCH localhost:8000/items/1 -H 'Content-Type: application/json' -d '{"quantity": 10}'
curl -X DELETE localhost:8000/items/1
```

## Test

```bash
pytest
```

`tests/test_items_api.py` exercises the HTTP layer end-to-end with FastAPI's `TestClient`;
`tests/test_store.py` covers the storage layer directly.
