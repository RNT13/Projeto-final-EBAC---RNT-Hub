SERVICE_NAME = web
PYTHON_EXEC = docker-compose exec $(SERVICE_NAME) poetry run python

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\n\033[1mComandos Disponíveis:\033[0m\n\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# Docker
up: ## 🚀 Build and up Docker containers
	docker-compose up -d --build

down: ## 🛑 Stop containers
	docker-compose down

logs: ## 📜 Tail logs
	docker-compose logs -f

shell: ## 💻 Shell into web container
	docker-compose exec $(SERVICE_NAME) /bin/sh

# Django
migrate: ## 🔁 Run migrations
	$(PYTHON_EXEC) manage.py makemigrations
	$(PYTHON_EXEC) manage.py migrate

createsuperuser: ## 👤 Create superuser (interactive)
	$(PYTHON_EXEC) manage.py createsuperuser

collectstatic: ## 📦 Collect static files
	$(PYTHON_EXEC) manage.py collectstatic --noinput

# Tests & QA
test: ## 🧪 Run tests (pytest)
	docker-compose exec $(SERVICE_NAME) poetry run pytest

format: ## 🎨 Format code (black + isort)
	docker-compose exec $(SERVICE_NAME) poetry run black .
	docker-compose exec $(SERVICE_NAME) poetry run isort .

lint: ## 🧐 Lint (flake8 + checks)
	docker-compose exec $(SERVICE_NAME) poetry run flake8 .
	docker-compose exec $(SERVICE_NAME) poetry run black --check .
	docker-compose exec $(SERVICE_NAME) poetry run isort --check .

reset: ## 🔥 Reset docker environment (use carefully)
	docker-compose down -v
	docker system prune -a --volumes -f
