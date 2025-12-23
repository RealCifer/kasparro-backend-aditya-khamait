# System Architecture – Kasparro Backend & ETL System

This document describes the architectural design, data flow, and key engineering decisions behind the Kasparro Backend & ETL System.

The goal of this system is to ingest data from multiple external sources, ensure reliability and auditability, normalize data for querying, and expose it via clean REST APIs.

---

## 1. High-Level Architecture

The system follows a layered backend + ETL architecture.

External APIs  
↓  
ETL Ingestion Services  
↓  
Raw Data Storage (per source)  
↓  
Normalized Data Layer  
↓  
API Layer (FastAPI)  

---

## 2. Core Components

### 2.1 API Layer (FastAPI)

Responsibilities:
- Exposes REST endpoints for health checks, ingestion, and data access
- Handles request validation and response formatting
- Does not contain business or ETL logic

Key Endpoints:
- GET /health
- POST /ingest/coinpaprika
- POST /ingest/coingecko
- GET /assets

---

### 2.2 ETL Layer (Services)

Each external data source has a dedicated ETL service.

Responsibilities:
- Fetch data from external APIs
- Retry failed API calls using exponential backoff
- Persist raw source data
- Normalize and upsert data into unified tables

ETL services:
- coinpaprika_ingest.py
- coingecko_ingest.py

ETL execution modes:
- Manual trigger via API
- Automatic execution via background scheduler

---

## 3. Data Architecture

### 3.1 Raw Data Tables (Source-Specific)

Each data source writes to its own raw table.

Tables:
- raw_coinpaprika
- raw_coingecko

Purpose:
- Preserve original data from external APIs
- Enable auditability and debugging
- Allow replay of ETL logic if schema changes

Raw tables are treated as append-only.

---

### 3.2 Normalized Table

Table:
- assets

Purpose:
- Unified schema for querying
- Optimized for API consumption
- Stores latest state of each asset

Behavior:
- Upsert logic ensures latest price is always available
- Source field tracks which API last updated the record

---

## 4. Reliability & Failure Recovery

The system is designed to be resilient to real-world failures.

### External API Failures
- Automatic retries with exponential backoff
- Timeouts enforced on API calls

### Database Failures
- Transactional writes using SQLAlchemy
- Rollbacks on failure prevent partial data writes
- Startup retry loop waits for database readiness

### Scheduler Isolation
- Background ETL scheduler runs independently of API requests
- ETL failures do not crash the API service

---

## 5. Containerization & Deployment

The entire system is containerized using Docker.

Containers:
- FastAPI application container
- PostgreSQL database container

Docker Compose:
- Manages service orchestration
- Ensures correct startup order
- Provides consistent local and production-like environments

---

## 6. Folder Structure Responsibility

core/
- Database setup
- ORM models
- Retry utilities
- Initialization logic

services/
- ETL ingestion logic
- Business logic
- Scheduler

schemas/
- API response models

main.py
- Application entry point
- API routing
- Startup lifecycle hooks

---

## 7. Design Principles Followed

- Separation of concerns
- Source-specific raw ingestion
- Transactional safety
- Idempotent ETL behavior
- Production-oriented error handling
- Infrastructure consistency via Docker

---

## 8. Summary

This architecture mirrors real-world backend and ETL systems by:
- Treating ingestion and serving as separate responsibilities
- Preserving raw data for auditing
- Normalizing data for efficient access
- Designing for failure and recovery
- Running in a fully containerized environment

The system is scalable, maintainable, and production-ready.
