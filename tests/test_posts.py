from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# A token to be used for testing.
TEST_TOKEN = "test-token"

def test_add_get_delete_post():
    headers = {"token": TEST_TOKEN}
    
    # Test add post
    response = client.post("/posts/add", json={"text": "Hello, world!"}, headers=headers)
    assert response.status_code == 200, f"Add post failed with status {response.status_code}"
    post_data = response.json()
    assert "postID" in post_data, "postID not returned"
    post_id = post_data["postID"]
    
    # Test get posts
    response = client.get("/posts/get", headers=headers)
    assert response.status_code == 200, f"Get posts failed with status {response.status_code}"
    posts = response.json()
    assert isinstance(posts, list), "Posts should be a list"
    
    # Test delete post
    response = client.delete(f"/posts/delete/{post_id}", headers=headers)
    assert response.status_code == 200, f"Delete post failed with status {response.status_code}"
