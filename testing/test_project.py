import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import uuid
import pytest

from python_project_management_cli_tool.models.project import Project

@pytest.fixture(autouse=True)
def clear_projects():
    # clears the projects list so the tests don't affect each other
    Project.clear_all()

def test_project_creation_with_defaults():
    p = Project(id=str(uuid.uuid4()), title="Website Redesign")
    
    assert p.title == "Website Redesign"
    assert p.description == ""
    assert p.due_date is None
    assert p.owner_user_id is None
    assert p.tasks == []
    assert p in Project.get_all()

def test_project_creation_auto_id():
    p = Project(id="", title="No ID Project")
    
    assert p.id != ""  # Should be auto-generated
    assert len(p.id) > 0
    assert p in Project.get_all()

def test_add_task():
    p = Project(id=str(uuid.uuid4()), title="Marketing Campaign")
    p.add_task("Create brochure")
    
    assert "Create brochure" in p.tasks

def test_remove_task():
    p = Project(id=str(uuid.uuid4()), title="App Launch")
    p.add_task("Book venue")
    p.remove_task("Book venue")
    
    assert "Book venue" not in p.tasks

def test_remove_task_not_in_list():
    p = Project(id=str(uuid.uuid4()), title="App Launch")
    p.remove_task("Non-existent")  # Should not raise error
    
    assert p.tasks == []

def test_find_by_title():
    p1 = Project(id=str(uuid.uuid4()), title="Onboarding Portal")
    p2 = Project(id=str(uuid.uuid4()), title="Onboarding Portal")
    p3 = Project(id=str(uuid.uuid4()), title="Training Platform")
    results = Project.find_by_title("Onboarding Portal")
    
    assert p1 in results
    assert p2 in results
    assert p3 not in results