import pytest

from app.models import ItemCreate, ItemUpdate
from app.store import ItemStore


@pytest.fixture
def store() -> ItemStore:
    return ItemStore()


def test_create_assigns_incrementing_ids(store):
    first = store.create(ItemCreate(name="a", price=1))
    second = store.create(ItemCreate(name="b", price=2))
    assert (first.id, second.id) == (1, 2)


def test_update_only_changes_provided_fields(store):
    item = store.create(ItemCreate(name="a", description="d", price=1, quantity=2))

    updated = store.update(item.id, ItemUpdate(quantity=5))
    assert updated.quantity == 5
    assert updated.description == "d"
    assert updated.created_at == item.created_at


def test_replace_resets_optional_fields(store):
    item = store.create(ItemCreate(name="a", description="d", price=1, quantity=2))

    replaced = store.replace(item.id, ItemCreate(name="b", price=3))
    assert replaced.description is None
    assert replaced.quantity == 0


def test_missing_item_operations_return_none(store):
    assert store.get(1) is None
    assert store.update(1, ItemUpdate(name="x")) is None
    assert store.replace(1, ItemCreate(name="x", price=1)) is None
    assert store.delete(1) is False


def test_clear_resets_ids(store):
    store.create(ItemCreate(name="a", price=1))
    store.clear()
    assert store.list() == []
    assert store.create(ItemCreate(name="b", price=1)).id == 1
