# tests/test_auth.py

from fastapi.testclient import TestClient
from app.main import app
from app.db.test_db import override_get_db, create_test_db, drop_test_db # Import test db functions
from app.db.session import get_db
import pytest
from app.models.user import User  # Import User model
from app.models.post import Post  # Import Post model

# Override the database dependency with the test database
app.dependency_overrides[get_db] = override_get_db

# Fixture to set up and tear down the test database
@pytest.fixture(scope="module")
def client():
    create_test_db()
    yield TestClient(app)
    drop_test_db()

def test_signup_and_login(client): # Added client as a fixture
    # Test signup
    response = client.post("/auth/signup", json={"email": "test1@example.com", "password": "secret123"})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    user_data = response.json()
    assert "id" in user_data, "User ID not returned"

    # Test login
    response = client.post("/auth/login", json={"email": "test1@example.com", "password": "secret123"})
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    token_data = response.json()
    assert "token" in token_data, "Token not returned"