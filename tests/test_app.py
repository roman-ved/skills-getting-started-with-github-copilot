from fastapi.testclient import TestClient

from src import app as app_module
from tests.conftest import create_test_client


def test_root_redirects_to_static_index() -> None:
    # Arrange
    client: TestClient = create_test_client()

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 302)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data() -> None:
    # Arrange
    client: TestClient = create_test_client()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]


def test_signup_adds_new_student_to_activity() -> None:
    # Arrange
    client: TestClient = create_test_client()
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    app_module.activities[activity_name]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_400_when_student_already_signed_up() -> None:
    # Arrange
    client: TestClient = create_test_client()
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_removes_registered_student() -> None:
    # Arrange
    client: TestClient = create_test_client()
    activity_name = "Chess Club"
    email = "registered.student@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email]

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_400_for_non_registered_student() -> None:
    # Arrange
    client: TestClient = create_test_client()
    activity_name = "Chess Club"
    email = "absent.student@mergington.edu"
    app_module.activities[activity_name]["participants"] = ["michael@mergington.edu"]

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"
