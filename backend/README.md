# IRSS COMMAND Backend API

FastAPI backend for IRSS COMMAND - Intent-Aware Railway Safety System

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ with PostGIS extension
- pip or poetry

### Installation

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Install PostgreSQL with PostGIS:**
   - Install PostgreSQL from https://www.postgresql.org/download/
   - Install PostGIS extension: `CREATE EXTENSION postgis;`
   - Create database: `CREATE DATABASE irss_command;`

5. **Run database migrations (when Alembic is configured):**
```bash
alembic upgrade head
```

6. **Run the server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── crud/         # CRUD operations
│   ├── config.py     # Configuration
│   ├── database.py   # Database connection
│   └── main.py       # FastAPI app
├── alembic/          # Database migrations
└── requirements.txt  # Dependencies
```

## API Endpoints

### Health Check
- `GET /health` - Health check
- `GET /` - API info

### Dashboard
- `GET /api/v1/dashboard/overview` - Dashboard overview
- `GET /api/v1/dashboard/system-status` - System status

### Tracks
- `GET /api/v1/tracks` - List track segments
- `GET /api/v1/tracks/{id}` - Get track segment
- `POST /api/v1/tracks` - Create track segment
- `PUT /api/v1/tracks/{id}` - Update track segment
- `GET /api/v1/tracks/{id}/sensors` - Get track sensors

### Sensors
- `GET /api/v1/sensors` - List sensors
- `GET /api/v1/sensors/{id}` - Get sensor
- `POST /api/v1/sensors` - Create sensor
- `GET /api/v1/sensors/{id}/readings` - Get sensor readings
- `POST /api/v1/sensors/readings` - Ingest sensor data

### Alerts
- `GET /api/v1/alerts` - List alerts
- `GET /api/v1/alerts/{id}` - Get alert
- `POST /api/v1/alerts` - Create alert
- `PUT /api/v1/alerts/{id}` - Update alert
- `POST /api/v1/alerts/{id}/acknowledge` - Acknowledge alert
- `POST /api/v1/alerts/{id}/resolve` - Resolve alert

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy app/
```

## TODO

- [ ] Setup Alembic migrations
- [ ] Implement authentication
- [ ] Add TimescaleDB for time-series data
- [ ] Implement ML/DL integration
- [ ] Add WebSocket support for real-time updates
- [ ] Add comprehensive error handling
- [ ] Add logging
- [ ] Add tests
- [ ] Add API rate limiting
- [ ] Add caching (Redis)

