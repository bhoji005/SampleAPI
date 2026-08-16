def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_item(client, sample_payload):
    response = client.post("/items", json=sample_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == sample_payload["name"]
    assert body["price"] == sample_payload["price"]
    assert body["created_at"] == body["updated_at"]


def test_create_item_validation_error(client):
    response = client.post("/items", json={"name": "", "price": -1})
    assert response.status_code == 422


def test_create_item_rejects_unknown_field(client, sample_payload):
    response = client.post("/items", json={**sample_payload, "colour": "red"})
    assert response.status_code == 422


def test_list_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_pagination(client, sample_payload):
    for index in range(5):
        client.post("/items", json={**sample_payload, "name": f"Item {index}"})

    response = client.get("/items", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Item 1", "Item 2"]


def test_get_item(client, sample_payload):
    item_id = client.post("/items", json=sample_payload).json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 not found"


def test_replace_item(client, sample_payload):
    item_id = client.post("/items", json=sample_payload).json()["id"]

    replacement = {"name": "Gadget", "price": 20.0, "quantity": 1}
    response = client.put(f"/items/{item_id}", json=replacement)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Gadget"
    assert body["description"] is None
    assert body["updated_at"] >= body["created_at"]


def test_replace_item_not_found(client, sample_payload):
    response = client.put("/items/42", json=sample_payload)
    assert response.status_code == 404


def test_partial_update_item(client, sample_payload):
    created = client.post("/items", json=sample_payload).json()

    response = client.patch(f"/items/{created['id']}", json={"quantity": 10})
    assert response.status_code == 200
    body = response.json()
    assert body["quantity"] == 10
    assert body["name"] == created["name"]
    assert body["description"] == created["description"]


def test_partial_update_item_not_found(client):
    response = client.patch("/items/42", json={"quantity": 1})
    assert response.status_code == 404


def test_delete_item(client, sample_payload):
    item_id = client.post("/items", json=sample_payload).json()["id"]

    assert client.delete(f"/items/{item_id}").status_code == 204
    assert client.get(f"/items/{item_id}").status_code == 404


def test_delete_item_not_found(client):
    assert client.delete("/items/42").status_code == 404


def test_full_crud_lifecycle(client, sample_payload):
    created = client.post("/items", json=sample_payload).json()
    item_id = created["id"]

    assert client.get("/items").json()[0]["id"] == item_id

    updated = client.patch(f"/items/{item_id}", json={"price": 1.5}).json()
    assert updated["price"] == 1.5

    assert client.delete(f"/items/{item_id}").status_code == 204
    assert client.get("/items").json() == []
