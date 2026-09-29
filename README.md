# StudyHub

StudyHub is a student productivity application that I am developing to strengthen my backend software engineering skills.

The project currently provides a REST API for creating, retrieving, updating and deleting study tasks, with data persisted in a PostgreSQL database.

## Tech Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Git & GitHub

## Current Features

- Create study tasks
- Retrieve all tasks
- Retrieve an individual task by ID
- Mark tasks as completed or incomplete
- Delete tasks
- PostgreSQL data persistence
- JSON request and response handling
- Input validation
- HTTP status code handling

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks` | Retrieve all tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/<task_id>` | Retrieve a specific task |
| PATCH | `/api/tasks/<task_id>` | Update a task's completion status |
| DELETE | `/api/tasks/<task_id>` | Delete a task |

## Example

Create a task:

POST `/api/tasks`

{
  "title": "Revise Computer Systems Architecture"
}

Response:

{
  "id": 1,
  "title": "Revise Computer Systems Architecture",
  "completed": false
}

## What I Have Learned

Building StudyHub has helped me develop practical experience with:

- Designing REST API endpoints
- HTTP methods and status codes
- JSON request and response handling
- Object-oriented programming
- Relational databases
- PostgreSQL
- SQLAlchemy ORM
- CRUD operations
- Input validation
- Git version control

## Planned Development

- Automated testing
- User accounts and authentication
- Improved project architecture
- Frontend interface
- Deployment