# Project: CLI Project Management Tool

## Overview
A command‑line tool for managing users, projects, and tasks. Admins can create/list users, assign projects to users, add tasks to projects, mark tasks complete, and persist everything to disk.

## Features
- Create/list users
- Create/list projects (per user)
- Create/list tasks (per project)
- Mark tasks complete / reopen
- Persist data to a local JSON file
- Clear, friendly CLI commands and help

## Future Improvements
- Search/filter (by status, due date, assignee)
- Edit/delete entities
- Import/export CSV
- Pretty output (tables, colors)

## Data Model
- User: `id`, `name`, `email`, `projects: [Project.id]`

- Project: `id`, `title`, `description`, `due_date`, `owner_user_id`, `tasks: [Task.id]`

- Task: `id`, `title`, `status (todo|in-progress|done)`, `assigned_to_user_id`, `project_id`

## Example CLI
```
pm add-user --name "Alex" --email "alex@example.com"
pm list-users
pm add-project --user "Alex" --title "CLI Tool" --desc "Project overview"
pm add-task --project "CLI Tool" --title "Implement add-task"
pm complete-task --id T-42
```

## Repo Structure
```
python_project_management_cli_tool/
├─ README.md
├─ requirements.txt            
├─ package                     # package
│  ├─ __init__.py
│  ├─ main.py                  # CLI entry point (argparse)
│  ├─ models/                  # raw data/class logic
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
│  └─ db.json                  # created at runtime
├─ testing/                    
│  └─ test_user.py
│  └─ test_project.py
│  └─ test_task.py
└─ scripts/
   └─ seeded-data-demo.py      # seeded data for demo
```