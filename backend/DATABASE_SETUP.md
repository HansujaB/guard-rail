# Database Setup Guide

## Prerequisites

1. **PostgreSQL 14+** installed
2. **PostGIS extension** installed
3. **Python 3.11+** with virtual environment

## Step 1: Install PostgreSQL with PostGIS

### Windows:
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Install PostgreSQL (remember your postgres user password)
3. Install PostGIS extension:
   - Open pgAdmin or psql
   - Connect to your PostgreSQL server
   - Run: `CREATE EXTENSION postgis;`

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install postgis postgresql-14-postgis-3
```

### macOS:
```bash
brew install postgresql
brew install postgis
```

## Step 2: Create Database

1. **Connect to PostgreSQL:**
```bash
psql -U postgres
```

2. **Create database:**
```sql
CREATE DATABASE irss_command;
```

3. **Connect to the database:**
```sql
\c irss_command
```

4. **Enable PostGIS extension:**
```sql
CREATE EXTENSION postgis;
CREATE EXTENSION "uuid-ossp";
```

5. **Verify extensions:**
```sql
\dx
```

You should see `postgis` and `uuid-ossp` in the list.

## Step 3: Setup Python Environment

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. **Copy environment example:**
```bash
cp env.example .env
```

2. **Edit `.env` file with your database credentials:**
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/irss_command
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:your_password@localhost:5432/irss_command

APP_NAME=IRSS COMMAND API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

CORS_ORIGINS=http://localhost:8080,http://localhost:3000

API_V1_PREFIX=/api/v1
```

**Important:** Replace:
- `your_password` with your PostgreSQL password
- `your-secret-key-here-change-in-production` with a secure random string

## Step 5: Run Database Migrations

1. **Create initial migration:**
```bash
alembic revision --autogenerate -m "Initial migration"
```

2. **Review the generated migration file:**
Check `alembic/versions/XXXX_initial_migration.py` to ensure it looks correct.

3. **Apply migrations:**
```bash
alembic upgrade head
```

This will create all the database tables.

## Step 6: Verify Database Tables

1. **Connect to database:**
```bash
psql -U postgres -d irss_command
```

2. **List tables:**
```sql
\dt
```

You should see tables:
- divisions
- track_segments
- sensors
- sensor_readings
- alerts
- incidents
- intent_analysis

3. **Check table structure:**
```sql
\d track_segments
\d sensors
\d alerts
\d intent_analysis
```

## Step 7: (Optional) Add Seed Data

You can add initial seed data for testing. Create a seed script if needed.

## Step 8: Start the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Error: "Extension postgis does not exist"
- Make sure PostGIS is installed
- Run: `CREATE EXTENSION postgis;` in your database

### Error: "Module 'geoalchemy2' not found"
- Make sure you've activated the virtual environment
- Run: `pip install geoalchemy2`

### Error: "Connection refused"
- Check if PostgreSQL is running
- Verify database credentials in `.env`
- Check if PostgreSQL is listening on port 5432

### Error: "Table already exists"
- If you need to reset, drop and recreate the database:
```sql
DROP DATABASE irss_command;
CREATE DATABASE irss_command;
\c irss_command
CREATE EXTENSION postgis;
CREATE EXTENSION "uuid-ossp";
```
Then run migrations again.

## Database Schema Overview

The database includes these main tables:

1. **divisions** - Railway divisions
2. **track_segments** - Track segments with geographic data (PostGIS)
3. **sensors** - Sensor devices deployed on tracks
4. **sensor_readings** - Time-series sensor data
5. **alerts** - Security alerts and notifications
6. **incidents** - Historical incident records
7. **intent_analysis** - ML model outputs and intent analysis results

All tables use UUID primary keys and include created_at/updated_at timestamps.

## Next Steps

After database setup:
1. Test API endpoints using `/docs`
2. Integrate ML models in `app/services/ml_service.py`
3. Connect frontend to backend APIs
4. Add authentication (if needed)

