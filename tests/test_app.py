from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_update_db_success():
    response = client.post("/update/1")
    assert response.status_code == 200
    assert "ETL pipeline trigger successful. " in response.json()["message"]


def test_update_db_fail():
    response = client.post("/update/i")
    assert response.status_code == 422


def test_search_data_text_success():
    body = {"text": "sleeveless pink A-line maxi dress", "type": "text"}
    response = client.post("/search", json=body)
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_search_data_image_success():
    body = {"text": "data/images/(BACKORDER)_ATHENA_EYELET_FLUTTER_SLEEVE_DRESS_NAVY_.jpg", "type": "image"}
    response = client.post("/search", json=body)
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_search_data_image_fail():
    body = {"text": "test/(BACKORDER)_ATHENA_EYELET_FLUTTER_SLEEVE_DRESS_NAVY_.jpg", "type": "image"}
    response = client.post("/search", json=body)
    assert response.status_code == 400
    assert response.json() == {"error": "Image path invalid"}


if __name__ == "__main__":
    print(__package__)
