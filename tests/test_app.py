from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]


def test_get_activities_returns_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_adds_participant():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Chess Club/unregister?email=daniel@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
