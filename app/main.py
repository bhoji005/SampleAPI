from fastapi import APIRouter, FastAPI, HTTPException, Query, Response, status

from app.models import Item, ItemCreate, ItemUpdate
from app.store import store

app = FastAPI(
    title="Sample CRUD API",
    description="A sample REST API demonstrating CRUD operations on items.",
    version="1.0.0",
)

router = APIRouter(prefix="/items", tags=["items"])


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("", response_model=list[Item])
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> list[Item]:
    return store.list(skip=skip, limit=limit)


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    return store.create(payload)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


@router.put("/{item_id}", response_model=Item)
def replace_item(item_id: int, payload: ItemCreate) -> Item:
    item = store.replace(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


@router.patch("/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    item = store.update(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> Response:
    if not store.delete(item_id):
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(router)
