import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# Ініціалізація мока для S3
@pytest.fixture
def mock_s3():
    with patch("main.s3") as mock:
        yield mock

# Створює bucket по POST запиту: /api/bucket/test123
def test_create_bucket_success(mock_s3):
    mock_s3.create_bucket.return_value = {}
    response = client.post("/api/bucket/test123")
    assert response.status_code == 200 # Має бути 200 OK
    assert response.json() == {"status": "created", "bucket": "test123"} # та відповідь зі статусом created
    mock_s3.create_bucket.assert_called_once_with(Bucket="test123")

# Створює ідентичний bucket попередньому
def test_create_bucket_failure(mock_s3):
    mock_s3.create_bucket.side_effect = Exception("Bucket exists") # Імітує помилку при створенні bucket
    response = client.post("/api/bucket/test123")
    assert response.status_code == 400 # Тоді має бути 400 Bad Request
    assert "Bucket exists" in response.json()["detail"] # + мають бути деталі помилки (Bucket exists)

# Отримання інфи GET запитом /api/bucket/test123
def test_get_bucket_info_success(mock_s3):
    mock_s3.list_objects_v2.return_value = {
        "Contents": [{"Size": 100}, {"Size": 200}],
        "KeyCount": 2,
    }
    response = client.get("/api/bucket/test123")
    assert response.status_code == 200 # Має бути 200 OK
    assert response.json() == {"bucket": "test123", "objects": 2, "size": 300} # та вивід самої інфи
    mock_s3.list_objects_v2.assert_called_once_with(Bucket="test123")

# Тест якщо bucket не існує
def test_get_bucket_info_not_found(mock_s3):
    mock_s3.list_objects_v2.side_effect = Exception("NoSuchBucket")
    response = client.get("/api/bucket/test123")
    assert response.status_code == 404 # Тоді має бути 400 Bad Request
    assert "NoSuchBucket" in response.json()["detail"] # + мають бути деталі помилки (NoSuchBucket)

# Видаляє bucket запитом DELETE /api/bucket/test123
def test_delete_bucket_success(mock_s3):
    mock_s3.delete_bucket.return_value = {}
    response = client.delete("/api/bucket/test123")
    assert response.status_code == 200 # Має бути 200 OK
    assert response.json() == {"status": "deleted", "bucket": "test123"} # та відповідь зі статусом deleted
    mock_s3.delete_bucket.assert_called_once_with(Bucket="test123")

# Тест якщо bucket не порожній при спробі видалення
def test_delete_bucket_failure(mock_s3):
    mock_s3.delete_bucket.side_effect = Exception("Bucket not empty")
    response = client.delete("/api/bucket/test123")
    assert response.status_code == 400 # Тоді має бути 400 Bad Request
    assert "Bucket not empty" in response.json()["detail"] # + мають бути деталі помилки (Bucket not empty)
