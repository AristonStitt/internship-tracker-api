# Internship Tracker API

A FastAPI backend API for tracking internship and job applications.

This project is a backend engineering practice project built around a realistic use case: storing, organizing, and managing internship/job applications. It includes database persistence, API validation, authentication, user-owned data, automated tests, Docker-based PostgreSQL setup, and GitHub Actions CI.

## Features

* FastAPI backend application
* PostgreSQL database
* SQLAlchemy ORM models
* Pydantic request/response validation
* Full CRUD for internship applications
* User registration and login
* JWT-based authentication
* User-owned application records
* Protected application routes
* Error handling for missing resources and invalid credentials
* Swagger/OpenAPI documentation
* pytest test suite
* GitHub Actions CI workflow

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* PyJWT
* pwdlib / Argon2 password hashing
* pytest
* Docker Compose
* GitHub Actions

## Project Structure

```text
internship-tracker-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── __init__.py
│       ├── applications.py
│       └── auth.py
│
├── tests/
│   ├── test_health.py
│   ├── test_applications.py
│   └── test_auth.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Core API Flow

```text
Client / Swagger UI
        ↓
FastAPI route
        ↓
Pydantic validation
        ↓
Authentication dependency
        ↓
SQLAlchemy model/session
        ↓
PostgreSQL database
        ↓
JSON response
```

## Authentication Flow

```text
User registers
        ↓
Password is hashed
        ↓
User logs in
        ↓
API returns JWT access token
        ↓
Client sends token in Authorization header
        ↓
Protected routes identify the current user
        ↓
User can only access their own applications
```

## Application Data Model

Example internship application:

```json
{
  "company": "Microsoft",
  "role": "Software Engineering Intern",
  "status": "applied",
  "location": "Remote",
  "application_url": "https://careers.microsoft.com",
  "date_applied": "2026-06-23",
  "notes": "Applied through careers page."
}
```

Allowed status values:

```text
wishlist
applied
interviewing
offer
rejected
```

## API Routes

### Health

| Method | Route     | Description                 |
| ------ | --------- | --------------------------- |
| GET    | `/health` | Check if the API is running |

### Auth

| Method | Route            | Description                           |
| ------ | ---------------- | ------------------------------------- |
| POST   | `/auth/register` | Register a new user                   |
| POST   | `/auth/login`    | Log in and receive a JWT access token |
| GET    | `/auth/me`       | Get the current authenticated user    |

### Applications

All application routes require authentication.

| Method | Route                            | Description                      |
| ------ | -------------------------------- | -------------------------------- |
| POST   | `/applications`                  | Create an application            |
| GET    | `/applications`                  | List current user's applications |
| GET    | `/applications/{application_id}` | Get one owned application        |
| PATCH  | `/applications/{application_id}` | Update one owned application     |
| DELETE | `/applications/{application_id}` | Delete one owned application     |

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/internship-tracker-api.git
cd internship-tracker-api
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create environment file

```bash
cp .env.example .env
```

Example `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/internship_tracker
SECRET_KEY=replace-this-with-a-real-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Start PostgreSQL with Docker Compose

```bash
docker compose up -d
```

### 6. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Run the test suite:

```bash
pytest
```

The tests cover:

* health check route
* user registration
* duplicate email handling
* login
* invalid login
* current-user route
* authentication-required application routes
* create application
* list applications
* get application
* update application
* delete application
* invalid application status
* user isolation between accounts

## GitHub Actions CI

This project includes a GitHub Actions workflow that runs tests automatically on:

* push to `main`
* pull request into `main`

The workflow starts a PostgreSQL service container, installs Python dependencies, sets test environment variables, and runs:

```bash
pytest
```

## What This Project Demonstrates

This project demonstrates core backend engineering skills:

* API design
* CRUD route implementation
* database modeling
* relational ownership between users and resources
* authentication and authorization
* password hashing
* JWT token handling
* request/response validation
* automated testing
* Docker-based local development
* CI automation with GitHub Actions

## Future Improvements

Possible next improvements:

* Alembic database migrations
* separate test database configuration
* pagination for application lists
* filtering by status/company/date
* sorting by date applied
* application deadline tracking
* resume/contact fields
* deployment to a cloud platform
* frontend dashboard
