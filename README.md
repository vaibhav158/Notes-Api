# Notes App (API)

Notes app backend _REST API_ is built with FastAPI framework with SQLite as database and deployed on the Heroku.


## Features 👓

- Easy structure
- Authentication
- Automatic and easy deployment to Heroku
- Test cases

## About this Project 💡

This project has two modules as following:

- **`data`**: Data source and operations.
- **`domain`**: Models and other common stuff.
- **`src`**: FastAPI application entry point and API routes.

## Development Setup 🖥

You will require Python version 3.6 or higher and you can use any IDE.

- Open this project in your preffered IDE.
- Open the terminal
- Set environment variables as following

```
SECRET_KEY=ANY_RANDOM_SECRET
```

- Run command `pip install -r requirements.txt`.
- After installation run command `aerich init -t src.database.db.TORTOISE_ORM`.
- Run command `aerich init-db`.
- And finally to run the server, run command `uvicorn src.main:app --reload`.
- Hit `http://127.0.0.1:8080/` and API will be live🔥.
- After running the server, go to `http://127.0.0.1:8080/docs` to test out APIs.

## Run Tests

- Run Auth Tests: `python -m pytest tests/test_auth.py`
- Run Index Tests: `python -m pytest tests/test_index.py`
- Run Note Tests: `python -m pytest tests/test_note.py`

## Built with 🛠

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework, high performance, easy to learn, fast to code, ready for production creating microservices, web applications, and more. It’s fun, free, and open source.
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/) - Tortoise ORM is an easy-to-use asyncio ORM (Object Relational Mapper) inspired by Django.
- [Aerich](https://github.com/tortoise/aerich) - Aerich is a database migrations tool for TortoiseORM, which is like alembic for SQLAlchemy, or like Django ORM with it's own migration solution.
- [Pytest](https://docs.pytest.org/) - The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.
- [SQLite] (https://sqlite.org/index.html) - SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.

# REST API Specification

## Authentication

### Register

```http
POST http://localhost:8080/auth/register
Content-Type: application/json

{
    "username": "test12345",
    "password": "12346789"
}

```

### Login

```http
POST http://localhost:8080/auth/login
Content-Type: application/json

{
    "username": "test12345",
    "password": "12346789"
}

```

## Note Operations

### Get all Notes

```http
GET http://localhost:8080/note/all
Content-Type: application/json
Authorization: Bearer YOUR_AUTH_TOKEN
```

### Create New Note

```http
POST http://localhost:8080/note/create
Content-Type: application/json
Authorization: Bearer YOUR_AUTH_TOKEN

{
  "title": "Hey there! This is title",
  "body": "Write note here..."
}
```

### Update Note

```http
PATCH http://localhost:8080/note/update
Content-Type: application/json
Authorization: Bearer YOUR_AUTH_TOKEN

{
  "title": "Updated title!",
  "body": "Updated body here..."
}
```

### Delete Note

```http
DELETE http://localhost:8080/note/delete?id=NOTE_ID_HERE
Content-Type: application/json
Authorization: Bearer YOUR_AUTH_TOKEN
```