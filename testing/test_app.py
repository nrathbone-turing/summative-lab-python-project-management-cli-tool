import sys
from pathlib import Path
import pytest
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.services.app import App
from python_project_management_cli_tool.models.user import User
from python_project_management_cli_tool.models.project import Project
from python_project_management_cli_tool.models.task import Task

@pytest.fixture(autouse=True)
def clear_all_models():
    User.clear_all()
    Project.clear_all()
    Task.all_tasks.clear()

def test_save_and_load(tmp_path, monkeypatch):
    db_file = tmp_path / "db.json"
    monkeypatch.setattr("python_project_management_cli_tool.store.json_store.DB_PATH", str(db_file))

    # Create some test data
    u = User("Alex", "alex@example.com")
    p = Project(title="Test Project")
    t = Task(title="Test Task", project_id=p.id)

    app = App()

    # Save to file
    app.save()

    # Ensure file got written
    assert db_file.exists()
    with open(db_file) as f:
        data = json.load(f)
    assert len(data["users"]) == 1
    assert len(data["projects"]) == 1
    assert len(data["tasks"]) == 1

    # Clear everything & reload
    User.clear_all()
    Project.clear_all()
    Task.all_tasks.clear()

    app.load()

    # ensure the data came back correctly
    assert len(User.get_all()) == 1
    assert len(Project.get_all()) == 1
    assert len(Task.get_all()) == 1
    assert User.get_all()[0].name == "Alex"
    assert Project.get_all()[0].title == "Test Project"
    assert Task.get_all()[0].title == "Test Task"

def test_save_and_load_preserves_ids(tmp_path, monkeypatch):
    db_file = tmp_path / "db.json"
    monkeypatch.setattr("python_project_management_cli_tool.store.json_store.DB_PATH", str(db_file))

    # Create objects with auto-generated ids
    u = User("Auto", "auto@example.com")
    p = Project(title="Auto Project")
    t = Task(title="Auto Task", project_id=p.id)

    original_ids = (u.id, p.id, t.id)  # store original ids

    app = App()
    app.save()

    # Clear and reload
    User.clear_all()
    Project.clear_all()
    Task.all_tasks.clear()

    app.load()

    # Fetch loaded objects
    loaded_u = User.get_all()[0]
    loaded_p = Project.get_all()[0]
    loaded_t = Task.get_all()[0]

    # Assert that ids match what was originally generated
    assert loaded_u.id == original_ids[0]
    assert loaded_p.id == original_ids[1]
    assert loaded_t.id == original_ids[2]