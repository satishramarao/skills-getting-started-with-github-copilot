import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test getting activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test signup for an activity
def test_signup_activity():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()

# Test unregister from an activity
def test_unregister_activity():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Ensure user is registered first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()

# Test error on unregistering non-existent participant
def test_unregister_nonexistent():
    activity = list(client.get("/activities").json().keys())[0]
    email = "notregistered@example.com"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "detail" in response.json()
