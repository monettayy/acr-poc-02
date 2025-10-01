.PHONY: run format test migrate clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  run      - Start the application with Docker Compose"
	@echo "  format   - Format code with black and check with flake8"
	@echo "  test     - Run tests"
	@echo "  migrate  - Run database migrations"
	@echo "  clean    - Clean up Docker containers and volumes"
	@echo "  help     - Show this help message"

# Start the application
run:
	docker-compose up --build

# Format and lint code
format:
	black app/ tests/ --line-length 88
	flake8 app/ tests/ --max-line-length 88 --extend-ignore E203,W503

# Run tests
test:
	pytest tests/ -v

# Run database migrations
migrate:
	alembic upgrade head

# Create a new migration
migrate-create:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

# Clean up Docker resources
clean:
	docker-compose down -v
	docker system prune -f

# Install dependencies locally (for development)
install:
	pip install -r requirements.txt

# Run the application locally (without Docker)
run-local:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
