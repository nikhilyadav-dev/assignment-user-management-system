# User Management API

A production-oriented REST API for managing users, built with **Flask** and **MySQL**.

The API provides user management, authentication, role-based authorization, search, pagination, validation, centralized error handling, database migrations, and application logging.

## Features

* RESTful JSON APIs for user management
* JWT-based authentication
* Role-based authorization
* Admin-only user creation
* Password hashing
* User search by name or email
* Pagination for user listing
* Email format validation
* Duplicate email handling
* User-not-found handling
* Centralized error handling
* Consistent API response format
* MySQL database integration
* Database migrations using Flask-Migrate/Alembic
* Environment-based configuration
* Application logging with rotating log files

## Tech Stack

| Technology         | Purpose                                |
| ------------------ | -------------------------------------- |
| Python             | Backend programming language           |
| Flask              | REST API framework                     |
| MySQL              | Relational database                    |
| Flask-SQLAlchemy   | ORM and database integration           |
| Flask-Migrate      | Database migration management          |
| Alembic            | Migration engine used by Flask-Migrate |
| Flask-JWT-Extended | JWT authentication and authorization   |
| PyMySQL            | MySQL database driver                  |
| Werkzeug           | Password hashing                       |
| python-dotenv      | Environment variable management        |

---

## Project Structure

```text
user-management-api/
│
├── app/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── user_service.py
│   │
│   ├── utils/
│   │   ├── auth.py
│   │   └── validators.py
│   │
│   ├── errors/
│   │   ├── exceptions.py
│   │   └── handlers.py
│   │
│   ├── __init__.py
│   ├── commands.py
│   ├── config.py
│   ├── extensions.py
│   └── logging_config.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── ...
│
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

### Architecture

The application follows a modular structure:

* **Routes** — Handles HTTP requests, authentication decorators, request parameters, and API responses.
* **Services** — Contains business logic and database operations.
* **Models** — Defines the database schema using SQLAlchemy.
* **Utils** — Contains reusable utilities such as validation and authorization helpers.
* **Errors** — Provides centralized application and API error handling.
* **Commands** — Contains Flask CLI commands such as database seeding.
* **Config** — Loads application and database configuration from environment variables.
* **Extensions** — Initializes Flask extensions such as SQLAlchemy, JWT, and Flask-Migrate.
* **Migrations** — Stores database schema migration history.

## Setup & Installation

### Prerequisites

Make sure the following are installed:

* Python 3.11+
* MySQL 8+
* Git

### 1. Clone the repository

```bash
git clone <repository-url>
cd user-management-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Create the database in MySQL:

```sql
CREATE DATABASE users;
```

### 5. Configure environment variables

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
SECRET_KEY=your-secret-key

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=users
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password

LOG_LEVEL=INFO

JWT_SECRET_KEY=your-jwt-secret-key
```

> Do not commit the `.env` file or real secrets to version control.

### 6. Run database migrations

Apply the existing database migrations:

```bash
flask db upgrade
```

### 7. Seed the initial admin user

```bash
flask seed
```

This creates the development admin account:

```text
Email: admin@example.com
Password: Admin@123
Role: admin
```

> The credentials above are intended for local development/testing only. Production credentials should be securely managed and must not use default values.

### 8. Start the application

```bash
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

## Authentication

The API uses **JWT (JSON Web Token)** for authentication.

### Authentication Flow

```text
POST /auth/login
       │
       ▼
Validate email & password
       │
       ▼
Verify password hash
       │
       ▼
Generate JWT access token
       │
       ▼
Client sends token with requests
       │
       ▼
Authorization: Bearer <token>
```

### Login

**Endpoint**

```http
POST /auth/login
```

**Request**

```json
{
  "email": "admin@example.com",
  "password": "Admin@123"
}
```

**Successful response**

```json
{
  "success": true,
  "data": {
    "access_token": "<JWT_TOKEN>"
  }
}
```

The access token expires after **1 hour**.

Protected endpoints require the token in the request header:

```http
Authorization: Bearer <JWT_TOKEN>
```

### Authorization

Authentication determines **who the user is**, while authorization determines **what the user is allowed to do**.

The API currently supports two roles:

* `admin`
* `user`

Only administrators can create new users.

```text
Admin JWT
   │
   ├── GET /users       → Allowed
   ├── GET /users/:id   → Allowed
   └── POST /users      → Allowed
                           
User JWT
   │
   ├── GET /users       → Allowed
   ├── GET /users/:id   → Allowed
   └── POST /users      → Forbidden (403)
```

## API Endpoints

### 1. Login

```http
POST /auth/login
```

Authenticates a user and returns a JWT access token.

**Authentication:** Not required

**Request body:**

```json
{
  "email": "admin@example.com",
  "password": "Admin@123"
}
```

**Response: `200 OK`**

```json
{
  "success": true,
  "data": {
    "access_token": "<JWT_TOKEN>"
  }
}
```

---

### 2. Create User

```http
POST /users
```

Creates a new user.

**Authentication:** Required

**Authorization:** Admin only

**Request body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "password": "John@123"
}
```

**Response: `201 Created`**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

The password is never returned in the API response.

---

### 3. Get Users

```http
GET /users
```

Returns a paginated list of users.

**Authentication:** Required

**Query parameters:**

| Parameter | Required | Default | Description               |
| --------- | -------- | ------: | ------------------------- |
| `search`  | No       |       — | Searches by name or email |
| `page`    | No       |     `1` | Page number               |
| `limit`   | No       |    `10` | Number of users per page  |

**Example:**

```http
GET /users?page=1&limit=10
```

**Response: `200 OK`**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Admin",
      "email": "admin@example.com",
      "role": "admin"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1
  }
}
```

---

### 4. Search Users

Users can be searched by name or email.

```http
GET /users?search=john
```

Search can also be combined with pagination:

```http
GET /users?search=john&page=1&limit=10
```

**Authentication:** Required

---

### 5. Get User by ID

```http
GET /users/<id>
```

Returns a single user by ID.

**Authentication:** Required

**Example:**

```http
GET /users/2
```

**Response: `200 OK`**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```
---

## Validation & Error Handling

The API validates incoming requests and returns consistent JSON error responses.

### Validation Rules

* `name`, `email`, `role`, and `password` are required when creating a user.
* Email format is validated before creating a user.
* Email addresses must be unique.
* User IDs must refer to an existing user.
* `page` must be greater than `0`.
* `limit` must be between `1` and `100`.
* Passwords are hashed before being stored in the database.
* Password hashes are never returned through the API.

### Error Response Format

All application errors follow a consistent structure:

```json id="ykx3sl"
{
  "success": false,
  "error": "User not found"
}
```

### Common HTTP Status Codes

| Status | Meaning                        | Example                     |
| -----: | ------------------------------ | --------------------------- |
|  `200` | Successful request             | Get users / login           |
|  `201` | Resource created               | Create user                 |
|  `400` | Validation error               | Invalid email               |
|  `401` | Authentication required/failed | Missing or invalid JWT      |
|  `403` | Insufficient permissions       | Non-admin creating a user   |
|  `404` | Resource not found             | User ID does not exist      |
|  `409` | Resource conflict              | Duplicate email             |
|  `500` | Unexpected server error        | Unhandled application error |

Unexpected server-side errors are logged while the API returns a generic `500 Internal Server Error` response to avoid exposing internal implementation details.

## Database

The application uses **MySQL** with **SQLAlchemy** as the ORM.

### Database

```text
users
```

### Users Table

| Column          | Type         | Constraints                 | Description     |
| --------------- | ------------ | --------------------------- | --------------- |
| `id`            | Integer      | Primary Key, Auto Increment | Unique user ID  |
| `name`          | VARCHAR(100) | Not Null                    | User's name     |
| `email`         | VARCHAR(255) | Not Null, Unique            | User's email    |
| `role`          | VARCHAR(50)  | Not Null                    | User role       |
| `password_hash` | VARCHAR(255) | Nullable                    | Hashed password |

`password_hash` is nullable to support the existing database migration history, but newly created users receive a password hash.

### Database Migrations

Database schema changes are managed using **Flask-Migrate/Alembic**.

Apply migrations with:

```bash id="j7m8f5"
flask db upgrade
```

Create a new migration after changing a model:

```bash id="q44e0s"
flask db migrate -m "Describe the change"
```

Review the generated migration before applying it.

## Logging

The application uses Python's logging system with a rotating file handler.

Logs are written to:

```text id="i7q4pv"
app.log
```

The logging configuration:

* Outputs logs to the console.
* Stores logs in a rotating file.
* Limits individual log file size.
* Keeps a limited number of backup log files.
* Logs unexpected application errors with stack traces.
* Keeps log files out of version control.

## Assumptions

The following assumptions were made while implementing the assignment:

1. **Role values** are stored as strings. The current implementation uses `admin` and `user`.
2. **User creation requires admin authorization.**
3. **JWT access tokens expire after 1 hour.**
4. **Logout/token revocation is not implemented**, since it was not required for the assignment.
5. **Refresh tokens are not implemented**; the current authentication flow uses access tokens only.
6. **Pagination defaults to 10 users per page**, with a maximum limit of 100.
7. **Passwords are required for newly created users** and are stored only as secure password hashes.
8. The seeded admin account is intended for local development/testing and should be replaced with securely managed credentials in a real production environment.

---

## Production Considerations

The current implementation is designed for the assignment requirements. For a larger production deployment, I would additionally consider:

* Run Flask behind a production WSGI server such as Gunicorn.
* Use HTTPS for all client-server communication.
* Store secrets using a secure secrets-management system rather than local `.env` files.
* Use a managed MySQL database with backups and monitoring.
* Configure database connection pooling appropriately for expected traffic.
* Add rate limiting, especially for authentication endpoints.
* Add automated unit and integration tests.
* Introduce refresh-token management and token revocation where required.
* Add structured logging and centralized log aggregation.
* Add application monitoring, metrics, and alerting.
* Containerize the application with Docker where appropriate.
* Add CI/CD pipelines for automated validation and deployment.
* Review database indexes and query performance as data volume grows.

## Assignment Questions

### 1. Why Flask/Django?

I chose **Flask** because the assignment primarily requires a lightweight REST API rather than a full-stack web application.

Flask provides the flexibility to design the application architecture around the assignment requirements while keeping the codebase small and modular.

For this project, Flask works well with:

* SQLAlchemy for database access
* Flask-Migrate for schema migrations
* Flask-JWT-Extended for authentication
* Python's built-in logging capabilities

Django would also be a suitable choice, particularly for applications that benefit from Django's built-in ORM, authentication system, admin interface, and broader framework conventions.

### 2. How would you scale this application?

The application can be scaled by separating application responsibilities and infrastructure components.

A possible architecture would be:

```text
                    Load Balancer
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          API #1      API #2      API #3
             │           │           │
             └───────────┼───────────┘
                         │
                    MySQL Database
                         │
                    Read Replicas
```

Depending on traffic and workload, additional improvements could include:

* Horizontal scaling of API instances.
* Load balancing between instances.
* Database indexing and query optimization.
* Read replicas for read-heavy workloads.
* Redis for caching and other shared temporary data.
* Background workers for asynchronous tasks.
* Centralized logging and monitoring.
* CDN/object storage for static or uploaded assets if introduced later.

### 3. What would you change for production?

For production, I would strengthen the application around security, reliability, observability, and deployment.

Key changes would include:

1. Run the application using a production WSGI server.
2. Enforce HTTPS.
3. Use secure secret management.
4. Add automated tests and CI/CD.
5. Add rate limiting and abuse protection.
6. Implement an appropriate refresh-token/revocation strategy.
7. Configure database backups and monitoring.
8. Add centralized structured logging.
9. Add metrics and health checks.
10. Containerize and deploy using an appropriate production infrastructure.

## AI Usage Declaration

AI tools were used during the development of this assignment as a development and learning aid.

### AI tools used

* ChatGPT

### Areas where AI assistance was used

AI assistance was used for:

* Understanding Flask and Python concepts.
* Designing the initial project structure.
* Reviewing implementation approaches.
* Debugging development issues.
* Suggesting code improvements and refactoring.
* Understanding JWT authentication and role-based authorization.
* Reviewing API behavior and edge cases.
* Assisting with README documentation.

### Manual work and modifications

The generated suggestions were reviewed and adapted to the assignment requirements. The implementation was manually configured, modified, run, and tested locally.

API behavior was manually verified for:

* Authentication
* Authorization
* User creation
* Duplicate emails
* Validation errors
* Search
* Pagination
* User lookup
* Missing/invalid/expired JWTs
* Consistent error responses


