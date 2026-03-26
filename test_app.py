import pytest
import os
from app import app, init_db

# Use a temporary test database
TEST_DB = "test_portfolio.db"


@pytest.fixture
def client():
    # Override database for testing
    app.config["TESTING"] = True

    # Replace DB file
    import app as myapp
    myapp.DB_NAME = TEST_DB

    # Initialize fresh DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db()

    with app.test_client() as client:
        yield client

    # Cleanup after test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# -------------------- TEST HOME --------------------
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


# -------------------- TEST HOME CONTENT --------------------
def test_home_content(client):
    response = client.get("/")
    assert b"Adithya Manuraj" in response.data


# -------------------- TEST ENQUIRY --------------------
def test_enquiry_submission(client):
    response = client.post("/enquiry", data={
        "name": "Test User",
        "email": "test@example.com",
        "message": "Hello"
    })

    # Should redirect after submission
    assert response.status_code == 302


# -------------------- TEST 404 --------------------
def test_invalid_route(client):
    response = client.get("/invalid")
    assert response.status_code == 404