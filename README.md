# HRMS Lite - Backend

Backend API for HRMS Lite (Human Resource Management System) built with FastAPI, SQLAlchemy, and SQLite.

## Tech Stack

- Framework: FastAPI 0.109.0
- Database: SQLite3 with SQLAlchemy ORM
- Python: 3.8+
- Validation: Pydantic v2
- Server: Uvicorn

## Project Structure

```
hrms_backend/
├── app/
│   ├── db/              - Database configuration and initialization
│   ├── models/          - SQLAlchemy models
│   ├── schemas/         - Pydantic schemas for validation
│   ├── repositories/    - Data access layer
│   ├── services/        - Business logic layer
│   ├── routers/         - API endpoints
│   └── main.py          - FastAPI application
├── requirements.txt
├── run.py              - Entry point
└── README.md
```

## Architecture

The project follows a layered architecture with SOLID principles:

1. Router Layer (routers/) - Handles HTTP requests and responses
2. Service Layer (services/) - Contains business logic and validation
3. Repository Layer (repositories/) - Manages database operations
4. Model Layer (models/) - SQLAlchemy database models
5. Schema Layer (schemas/) - Pydantic models for validation

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/api/docs

## API Endpoints

### Employee Management

- POST /api/employees/ - Create a new employee
- GET /api/employees/ - Get all employees
- GET /api/employees/{employee_id} - Get employee by ID
- DELETE /api/employees/{employee_id} - Delete an employee

### Attendance Management

- POST /api/attendance/ - Mark attendance
- GET /api/attendance/ - Get all attendance records
- GET /api/attendance/employee/{employee_id} - Get attendance by employee

## Example Requests

### Create Employee

```bash
curl -X POST "http://localhost:8000/api/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering"
  }'
```

### Mark Attendance

```bash
curl -X POST "http://localhost:8000/api/attendance/" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "date": "2026-01-28",
    "status": "Present"
  }'
```

## Database

The application uses SQLite database (hrms.db) which is created automatically on first run.

### Schema

Employees Table:
- employee_id (Primary Key)
- full_name
- email (Unique)
- department

Attendance Table:
- id (Primary Key, Auto-increment)
- employee_id (Foreign Key)
- date
- status (Present/Absent)

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure build settings:
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

## Environment Variables

- DATABASE_URL: Database connection string (default: sqlite:///./hrms.db)

## Error Handling

The API implements comprehensive error handling:
- 400 Bad Request: Duplicate employee, invalid data
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation errors
- 500 Internal Server Error: Server errors

All errors return meaningful JSON responses with details.

