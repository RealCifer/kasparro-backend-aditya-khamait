# Backend & ETL System

This project is a production-grade backend and ETL system built as part of the Backend project.  
It demonstrates real-world backend engineering practices such as data ingestion, failure recovery, clean architecture, and containerized deployment.

The system ingests cryptocurrency market data from multiple external APIs, stores raw data per source, normalizes it into a unified schema, and exposes it via REST APIs.

---

## Tech Stack

- FastAPI – Backend framework
- PostgreSQL – Relational database
- SQLAlchemy – ORM & transaction management
- Docker & Docker Compose – Containerization
- CoinPaprika API – Market data source
- CoinGecko API – Market data source

---

## Architecture Overview

### High-Level Flow

External APIs  
↓  
ETL Services (with retries & recovery)  
↓  
Raw Tables (source-specific)  
- raw_coinpaprika  
- raw_coingecko  
↓  
Normalized Table  
- assets  
↓  
FastAPI Endpoints  

---

## Database Design

### Raw Tables (Audit & Replay)
Each external data source has its own raw table:
- raw_coinpaprika
- raw_coingecko

These tables store immutable ingestion data and allow:
- Auditing external data
- Debugging ingestion issues
- Replaying ETL logic if needed

### Normalized Table
- assets
- Unified schema for API consumption
- Upsert logic ensures latest prices
- Source column tracks data origin

---

## ETL Design

- Each ETL pipeline:
  - Fetches data from external API
  - Retries failed API calls using exponential backoff
  - Stores raw data in source-specific tables
  - Normalizes data into the assets table
- ETL execution modes:
  - Manual trigger via API endpoints
  - Automatic execution via background scheduler

---

## Reliability & Recovery

- Retry logic with exponential backoff for external APIs
- Database transactions with rollback on failure
- Startup retry loop waits for database readiness
- Scheduler isolated from API layer to prevent crashes

---

## API Endpoints

### Health Check
GET /health

### Manual ETL Triggers
POST /ingest/coinpaprika  
POST /ingest/coingecko  

### Data Access
GET /assets?limit=10&offset=0

---

## Running the Project

### Prerequisites
- Docker
- Docker Compose

### Start the system
docker-compose up --build

### Swagger UI
http://localhost:8000/docs

---

## Verifying Data Ingestion

Enter PostgreSQL container:
docker exec -it kasparro-postgres psql -U postgres -d etl_db

List tables:
\dt

Verify raw ingestion:
SELECT COUNT(*) FROM raw_coinpaprika;
SELECT COUNT(*) FROM raw_coingecko;

Verify normalized data:
SELECT source, COUNT(*) FROM assets GROUP BY source;

## CSV Ingestion

The system supports ingestion from a local CSV source.

### File:

### Endpoint:

### Description:
Reads asset data from CSV and normalizes it into the unified `assets` table.

---

## Project Structure

core/
- db.py
- init_db.py
- models.py
- retry.py

services/
- coinpaprika_ingest.py
- coingecko_ingest.py
- asset_service.py
- scheduler.py

schemas/
- asset.py

main.py  
Dockerfile  
docker-compose.yml  
requirements.txt  
README.md  

---

## Outcome

This project demonstrates:
- Multi-source ETL pipelines
- Clean backend architecture
- Failure recovery and retries
- Dockerized deployment
- Production-style data modeling

The system closely mirrors real-world backend and ETL engineering workflows.

# Backend – Live URLs

## Deployed Backend (Render)
https://kasparro-backend-4y2n.onrender.com

---

## Health Check
https://kasparro-backend-4y2n.onrender.com/health

---

## API Documentation (Swagger UI)
https://kasparro-backend-4y2n.onrender.com/docs

---

## ETL Ingestion Endpoints

### CoinPaprika
POST  
https://kasparro-backend-4y2n.onrender.com/ingest/coinpaprika?limit=50

### CoinGecko
POST  
https://kasparro-backend-4y2n.onrender.com/ingest/coingecko?limit=50

---

## Assets API
GET  
https://kasparro-backend-4y2n.onrender.com/assets?limit=10&offset=0

