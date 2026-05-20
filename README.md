# IoT Device Management API

A robust FastAPI-based system for managing IoT devices, sensors, and organizations. This project follows the **MVC (Model-View-Controller)** pattern to keep models, business logic, and presentation concerns separated.

## 🚀 Overview

The API lets you register organizations, manage devices and sensors, ingest and query readings, and handle alerts triggered by device conditions. The project includes a small authentication layer for user management and token-based access control used by the frontend.

### Key Features
- **MVC Architecture**: Clear separation:
   - **Models**: `dal` (Data Access Layer)
   - **Controllers/Logic**: `bll` (Business Logic Layer)
   - **Views/Presentation**: `presentation` (FastAPI routers and DI)
- **Device & Sensor Management**: Full CRUD for organizations, devices, sensors, readings, and alerts.
- **Auth & Users**: User creation, password hashing (bcrypt), and JWT-based access tokens for protected endpoints.
- **Data Import**: `importer.py` can generate and populate sample readings for testing.
- **Async DB**: Async SQLAlchemy sessions (for `asyncpg`/Postgres).

---

## 🛠️ Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy (async)
- **Auth**: `python-jose` for JWTs, `passlib` for password hashing
- **Database**: PostgreSQL via `asyncpg`

---

## 📋 Prerequisites
- **Python**: 3.13+
- **Postgres**: running instance and connection configured in `dal` settings

---

## ⚙️ Installation & Setup

1. Clone the repo and change directory:
```bash
git clone <repository-url>
cd mvc
```

2. Install dependencies (this project uses `uv`):
```bash
uv sync
```

---

## 🏃 Running the Application

Initialize the database (drops and recreates schema, then inserts sample data):
```bash
uv run importer.py
```

Start the API server:
```bash
uv run uvicorn main:app --reload
```

---

## 📖 API Documentation
Open the interactive docs when the server is running:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Presentation Layer Details

- **`presentation/dependencies.py`**: Provides FastAPI dependency providers used by routers, including `get_db_session` and service factories (`get_organizations_service`, `get_devices_service`, `get_sensors_service`, `get_alerts_service`, `get_readings_service`, `get_users_service`). These create repository instances and wire them into BLL services using the async DB `Session`.

- **Routers (`presentation/routers/`)**: Exposes the API endpoints grouped by resource:
   - `/organizations` — CRUD for organizations
   - `/devices` — CRUD for devices
   - `/sensors` — CRUD for sensors
   - `/readings` — CRUD for readings plus `GET /readings/between-dates` (accepts `start`, `end`, `limit`, `offset`)
   - `/alerts` — CRUD for alerts
   - `/users` — user info endpoint (requires authenticated user)
   - `/auth` — authentication endpoints (create user, token)

- **Response models**: Routers use Pydantic models with `ConfigDict(from_attributes=True)` to serialize ORM-style objects returned from services.

---

## Frontend & Authorization

- **Frontend pages**: The system is intended to be consumed by a frontend application which typically includes:
   - **Login** — authenticate users and obtain an access token
   - **User Profile** — display current user and role
   - **Dashboard** — organization overview, recent readings, and alerts
   - **Resource pages** — Organizations, Devices, Sensors, Readings, Alerts (CRUD)

- **Auth flow (API)**:
   - `POST /auth/` — create a new user (passwords are hashed with bcrypt before persisting).
   - `POST /auth/token` — OAuth2 password flow endpoint that returns a Bearer JWT (expires after 30 minutes by default).
   - `get_current_user` dependency — decodes the JWT and exposes `username`, `user_id`, `organization_id`, and `role` to protected endpoints.

- **How frontend uses auth**: Frontend should call `/auth/token` with username/password to receive an access token, then include the header `Authorization: Bearer <token>` on protected requests. Endpoints will return `401` for invalid/missing tokens and `403` when a user lacks required permissions.

---

## 📁 Project Structure & MVC Mapping
```text
├── bll/            # Business Logic Layer (Services, Exceptions)
├── dal/            # Data Access Layer (Models, Repositories, DB connection)
├── presentation/   # Presentation Layer (API Routers, Dependencies)
├── generator/      # Utility for generating synthetic CSV data
├── main.py         # Application entry point
├── importer.py     # Database initialization and data import script
└── readings.csv    # Generated sample data
```
