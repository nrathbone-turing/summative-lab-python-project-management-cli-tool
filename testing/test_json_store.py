# testing/models/test_json_store.py
import sys
from pathlib import Path
import os
import json
import tempfile
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.store import json_store as store

def test_read_nonexistent_file(monkeypatch):
    # Point DB_PATH to a non-existent temp file
    tmpfile = Path(tempfile.gettempdir()) / "nonexistent.json"
    monkeypatch.setattr(store, "DB_PATH", str(tmpfile))

    result = store._read()
    assert result == {"users": [], "projects": [], "tasks": []}

def test_write_and_read_round_trip(tmp_path, monkeypatch):
    # Use a temp file path for DB
    db_file = tmp_path / "db.json"
    monkeypatch.setattr(store, "DB_PATH", str(db_file))

    # Write sample data
    data = {"users": [{"_id": "1", "name": "Alex"}], "projects": [], "tasks": []}
    store._write(data)

    # Ensure file exists and has correct JSON
    assert db_file.exists()
    with open(db_file) as f:
        assert json.load(f) == data

    # Now test reading back
    result = store._read()
    assert result == data

def test_save_and_load_all(tmp_path, monkeypatch):
    # Point DB_PATH to a temp file
    db_file = tmp_path / "db.json"
    monkeypatch.setattr(store, "DB_PATH", str(db_file))

    # Dummy classes with all needed attributes for save_all()
    class DummyUser:
        def __init__(self, _id):
            self._id = _id
            self.name = "Test User"
            self.email = "test@example.com"
            self.projects = []

    class DummyProject:
        def __init__(self, _id):
            self._id = _id
            self.title = "Test Project"
            self.description = ""
            self.due_date = None
            self.owner_user_id = None
            self.tasks = []

    class DummyTask:
        def __init__(self, _id):
            self._id = _id
            self.title = "Test Task"
            self.description = ""
            self.due_date = None
            self.completed = False
            self.project_id = None
    
    users = [DummyUser("u1")]
    projects = [DummyProject("p1")]
    tasks = [DummyTask("t1")]

    # Save and load
    store.save_all(users, projects, tasks)
    loaded_users, loaded_projects, loaded_tasks = store.load_all()

    assert loaded_users[0]["id"] == "u1"
    assert loaded_projects[0]["id"] == "p1"
    assert loaded_tasks[0]["id"] == "t1"