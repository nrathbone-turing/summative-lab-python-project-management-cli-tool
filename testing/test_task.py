# testing/models/test_task.py
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.models.task import Task

@pytest.fixture(autouse=True)
def _clear_tasks():
    # clears the tasks list so the tests don't affect each other
    Task.clear_all()

def test_task_creation():
    t = Task(title="Test Task", description="Do something")
    # due_date must be set via property or set_due_date (validated)
    t.set_due_date("2025-08-15")
    
    assert t.title == "Test Task"
    assert t.description == "Do something"
    assert t.due_date == "2025-08-15"
    assert t.completed is False
    assert t in Task.get_all()

def test_mark_complete_and_incomplete():
    t = Task(title="Another Task")
    assert not t.completed
    
    t.mark_complete()
    assert t.completed
    
    t.mark_incomplete() 
    assert not t.completed

def test_set_due_date_valid():
    t = Task(title="Due Date Task")
    t.set_due_date("2025-09-01")
    
    assert t.due_date == "2025-09-01"

def test_set_due_date_invalid():
    t = Task(title="Invalid Date Task")
    with pytest.raises(ValueError):
        t.set_due_date("01-09-2025")  # invalid format

def test_find_by_project():
    p_id = "project-123"
    t1 = Task(title="P Task 1", project_id=p_id)
    t2 = Task(title="P Task 2", project_id=p_id)
    t3 = Task(title="Other Task", project_id="other-id")
    result = Task.find_by_project(p_id)
    
    assert t1 in result and t2 in result and t3 not in result