import pytest

from app import create_app
from extensions import db

@pytest.fixture
def client():
    app = create_app("sqlite:///:memory:")

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

def test_api_status(client):

    response = client.get("/api/status")

    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "StudyHub"
    assert data["status"] == "running"
    assert data["version"] == 0.1

def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Revise Computer Systems"}
    )

    data = response.get_json()

    assert response.status_code == 201
    assert isinstance(data["id"],int)
    assert data["title"] == "Revise Computer Systems"
    assert data["completed"] is False

def test_get_tasks_by_id(client):
    

    create_response = client.post(
        "/api/tasks",
        json = {"title":"Learn SQL"}
    )
    created_task = create_response.get_json()
    task_id = created_task["id"]
    
    response = client.get(f"/api/tasks/{task_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == task_id
    assert data["title"] == "Learn SQL"
    assert data["completed"] is False

    