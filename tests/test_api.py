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

def test_get_tasks(client):

    create_response = client.post(
        "/api/tasks",
        json = {"title":"Learn pytest"}
    )

    created_task = create_response.get_json()
    task_id = created_task["id"]

    Create_response = client.post(
        "/api/tasks",
        json = {"title":"Learn NumPy"}
    )

    Created_task = Create_response.get_json()


    response = client.get(f"/api/tasks")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[1]["id"] == 2
    assert data[1]["title"] == "Learn NumPy"  


def test_update_task(client):

    create_response = client.post(
    f"/api/tasks",
    json = {"title":"Learn NumPy"}
    )

    create_task = create_response.get_json()
    task_id = create_task["id"]

    alter_response = client.patch(
    f"/api/tasks/{task_id}",
    json = {"completed":True}
    )

    data = alter_response.get_json()

    assert alter_response.status_code == 200
    assert data["completed"] == True

    get_response = client.get(f"/api/tasks/{task_id}")
    get_data = get_response.get_json()

    assert get_response.status_code == 200
    assert get_data["completed"] == True


def test_delete_task(client):
    # Arrange: create a task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Learn PyTorch"}
    )

    created_task = create_response.get_json()
    task_id = created_task["id"]

    # Act: delete the task
    delete_response = client.delete(f"/api/tasks/{task_id}")

    # Assert: deletion succeeded
    assert delete_response.status_code == 200

    # Verify: the task no longer exists
    get_response = client.get(f"/api/tasks/{task_id}")

    assert get_response.status_code == 404




    