.PHONY: up down logs api

up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

api:
	uvicorn main:app --host 0.0.0.0 --port 8000
