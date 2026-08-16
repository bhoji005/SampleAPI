from threading import Lock

from app.models import Item, ItemCreate, ItemUpdate, utcnow


class ItemStore:
    """Thread-safe in-memory storage for items."""

    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._next_id = 1
        self._lock = Lock()

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            self._next_id = 1

    def list(self, skip: int = 0, limit: int = 50) -> list[Item]:
        with self._lock:
            items = [self._items[key] for key in sorted(self._items)]
        return items[skip : skip + limit]

    def get(self, item_id: int) -> Item | None:
        with self._lock:
            return self._items.get(item_id)

    def create(self, payload: ItemCreate) -> Item:
        now = utcnow()
        with self._lock:
            item = Item(
                id=self._next_id,
                created_at=now,
                updated_at=now,
                **payload.model_dump(),
            )
            self._items[item.id] = item
            self._next_id += 1
        return item

    def replace(self, item_id: int, payload: ItemCreate) -> Item | None:
        with self._lock:
            existing = self._items.get(item_id)
            if existing is None:
                return None
            item = Item(
                id=item_id,
                created_at=existing.created_at,
                updated_at=utcnow(),
                **payload.model_dump(),
            )
            self._items[item_id] = item
        return item

    def update(self, item_id: int, payload: ItemUpdate) -> Item | None:
        with self._lock:
            existing = self._items.get(item_id)
            if existing is None:
                return None
            changes = payload.model_dump(exclude_unset=True)
            item = existing.model_copy(update={**changes, "updated_at": utcnow()})
            self._items[item_id] = item
        return item

    def delete(self, item_id: int) -> bool:
        with self._lock:
            return self._items.pop(item_id, None) is not None


store = ItemStore()
