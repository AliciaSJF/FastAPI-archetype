"""
Tests de ejemplo para la aplicación
"""
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_read_root():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test del endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_user():
    """Test de creación de usuario"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["username"] == user_data["username"]


def test_get_users():
    """Test de obtención de usuarios"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

