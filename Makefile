.PHONY: help up down run build etl logs clean

APP_NAME=kasparro-backend
PORT=8000

help:
	@echo "Kasparro Backend Makefile"
	@echo ""
	@echo "make run        → Run API locally"
	@echo "make build      → Build docker image"
	@echo "make up         → Start services with docker-compose"
	@echo "make down       → Stop services"
	@echo "make etl        → Trigger ETL manually"
	@echo "make logs       → View docker logs"
	@echo "make clean      → Cleanup containers & images"

run:
	uvicorn main:app --host 0.0.0.0 --port $(PORT) --reload

build:
	docker build -t $(APP_NAME) .

up:
	docker-compose up --build

down:
	docker-compose down

etl:
	curl -X POST http://localhost:$(PORT)/ingest/coinpaprika
	curl -X POST http://localhost:$(PORT)/ingest/coingecko

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f
