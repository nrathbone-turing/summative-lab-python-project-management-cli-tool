# testing/models/test_project.py
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.models.project import Project

@pytest.fixture(autouse=True)
def clear_projects():
    # clears the projects list so the tests don't affect each other
    Project.clear_all()

def test_project_creation_with_defaults():
    p = Project(title="Website Redesign")
    
    assert p.title == "Website Redesign"
    assert p.description == ""
    assert p.due_date is None
    assert p.owner_user_id is None
    assert p.tasks == []
    assert p in Project.get_all()

def test_add_task():
    p = Project(title="Marketing Campaign")
    p.add_task("Create brochure")
    
    assert "Create brochure" in p.tasks

def test_remove_task():
    p = Project(title="App Launch")
    p.add_task("Book venue")
    
    assert p.remove_task("Book venue") is True
    
    assert "Book venue" not in p.tasks

def test_remove_task_not_in_list():
    p = Project(title="App Launch")
    
    assert p.remove_task("Non-existent") is False
    
    assert p.tasks == []

def test_find_by_title():
    p1 = Project(title="Onboarding Portal")
    p2 = Project(title="Onboarding Portal")
    p3 = Project(title="Training Platform")
    results = Project.find_by_title("Onboarding Portal")
    
    assert p1 in results and p2 in results and p3 not in results