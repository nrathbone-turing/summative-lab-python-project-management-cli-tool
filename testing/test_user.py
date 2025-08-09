import sys
from pathlib import Path
import pytest
sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.models.user import User

@pytest.fixture(autouse=True)
# clears the all_users list so the tests don't affect each other
def clear_users():
    User.clear_all()

def test_user_creation():
    # Create a user and check that attributes match
    u = User("1", "Alex", "alex@example.com")
    
    assert u.id == "1"
    assert u.name == "Alex"
    assert u.email == "alex@example.com"
    assert u.projects == []
    assert u in User.get_all()

def test_add_project():
    # Create a user
    u = User("2", "Jordan", "jordan@example.com")
    # Add a project
    project = "DummyProject"
    u.add_project(project)
    
    assert project in u.projects

def test_remove_project():
    u = User("3", "Taylor", "taylor@example.com")
    u.add_project("Proj1")
    
    # Should return True and remove it
    assert u.remove_project("Proj1") is True
    assert "Proj1" not in u.projects
    # Should return False since it’s gone
    assert u.remove_project("ProjX") is False

def test_str_representation():
    u = User("4", "Alex", "alex@example.com")
    # str(u) should match the custom human readable __str__ format
    assert str(u) == "User: Alex (alex@example.com)"

def test_find_by_email():
    u = User("5", "Sam", "sam@example.com")
    # Should find the existing user
    found = User.find_by_email("sam@example.com")
    assert found is u
    # Should return None if email doesn't exist
    assert User.find_by_email("nope@example.com") is None