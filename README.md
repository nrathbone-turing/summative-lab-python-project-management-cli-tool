# Project: CLI Project Management Tool

## Overview
A command‑line tool for managing users, projects, and tasks. 
Admins can create and list entities, assign projects to users, add tasks to projects, mark tasks complete, and persist everything to disk via a JSON store.

The tool is built with Python dataclasses for core models, a dedicated JSON persistence layer, and a service layer (`App`) that coordinates save/load operations across all models.

## Features
- Create and list users, projects, and tasks.
- Assign projects to specific users.
- Add tasks to projects and optionally link them to a user.
- Mark tasks complete or reopen them.
- Persist all data to a local JSON file with ID preservation across sessions.
- Due date support for tasks, with validation (`YYYY-MM-DD` format).
- Clear, friendly CLI commands and help text.

## Future Improvements
- Search/filter (by status, due date, assignee)
- Edit/delete entities
- Import/export CSV
- Pretty output (tables, colors)

## Data Model
### User
```
{
  "id": "UUID",
  "name": "string",
  "email": "string",
  "projects": ["project_id", ...]
}
```

### Project
```
{
  "id": "UUID",
  "title": "string",
  "description": "string",
  "due_date": "YYYY-MM-DD or null",
  "owner_user_id": "user_id or null",
  "tasks": ["task_id", ...]
}
```

### Task
```
{
  "id": "UUID",
  "title": "string",
  "description": "string",
  "due_date": "YYYY-MM-DD or null",
  "completed": true|false,
  "project_id": "project_id or null"
}
```
## Example CLI
```
pm add-user --name "Alex" --email "alex@example.com"
pm list-users
pm add-project --user "Alex" --title "CLI Tool" --desc "Project overview"
pm add-task --project "CLI Tool" --title "Implement add-task" --due "2025-09-01"
pm complete-task --id T-42
pm save
pm load
```

## Repo Structure
```
python_project_management_cli_tool/
├─ README.md
├─ requirements.txt
├─ python_project_management_cli_tool/
│  ├─ __init__.py
│  ├─ main.py                  # CLI entry point (argparse)
│  ├─ models/                  # core data models
│  │  ├─ __init__.py
│  │  ├─ user.py
│  │  ├─ project.py
│  │  └─ task.py
│  ├─ store/                   # persistence (JSON I/O)
│  │  ├─ __init__.py
│  │  └─ json_store.py
│  └─ services/                # app/use-case layer
│     ├─ __init__.py
│     └─ app.py
├─ data/
│  └─ db.json                  # created/updated at runtime
└─ testing/
   ├─ test_user.py
   ├─ test_project.py
   ├─ test_task.py
   ├─ test_app.py
   └─ test_json_store.py
```

## Persistence Flow Diagram
```
┌──────────────┐
│   CLI User   │
└──────┬───────┘
       │ issues save/load command
       ▼
┌──────────────┐
│     App      │  (services/app.py)
└──────┬───────┘
       │ calls save_all() or load_all()
       ▼
┌────────────────┐
│  json_store.py │  (store/json_store.py)
├────────────────┤
│ save_all()     │ → Serializes all User/Project/Task objects to dicts and writes to db.json
│ load_all()     │ → Reads db.json, returns raw dicts for each model type
└──────┬─────────┘
       │
       ▼
┌──────────────┐
│   Models     │  (dataclass instances rehydrated from JSON data)
│  user.py     │
│  project.py  │
│  task.py     │
└──────────────┘
```