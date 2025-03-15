# tests/test_posts.py
from fastapi.testclient import TestClient
from app.main import app
from app.db.test_db import override_get_db, create_test_db, drop_test_db
from app.db.session import get_db
import pytest

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

# Fixture to set up and tear down the test database and get a token
@pytest.fixture(scope="module")
def test_setup():
    create_test_db()
    client = TestClient(app)

    # Create a user and get a token
    signup_response = client.post("/auth/signup", json={"email": "testuser@example.com", "password": "testpassword"})
    assert signup_response.status_code == 200
    print('-------------hi------------')
    login_response = client.post("/auth/login", json={"email": "testuser@example.com", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    yield client, token  # Yield both client and token
    drop_test_db()

def test_add_get_delete_post(test_setup):
    client, token = test_setup  # Unpack client and token
    headers = {"token": token}  # Use the obtained token

    # Test add post
    response = client.post("/posts/add", json={"text": "Hello, world!"}, headers=headers)
    assert response.status_code == 200, f"Add post failed with status {response.status_code}"
    post_data = response.json()
    post_id = post_data["id"]

    # Test get post
    response = client.get(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200, f"Get post failed with status {response.status_code}"
    retrieved_post = response.json()
    assert retrieved_post["text"] == "Hello, world!", "Incorrect post text retrieved"

    # Test delete post
    response = client.delete(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200, f"Delete post failed with status {response.status_code}"

    # Verify post is deleted
    response = client.get(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 404, "Post was not deleted"