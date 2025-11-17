# 🐍 Guia Rápido --- Criação de Backend Django com Poetry + Docker + Render

Este é um tutorial rápido, direto e profissional para criar um **backend
Django moderno**, usando:

- **Poetry** (gerenciador de dependências)
- **Django + DRF**
- **Docker**
- **Render** (deploy)
- **GitHub**
- **GitHub Actions**
- **Docker Compose**
- **CI/CD**
- **Makefile**

---

# ✅ 0. Pré‑requisitos

- Python 3.12 ou 3.13 instalado\
- Poetry instalado\
- Docker Desktop instalado

---

# 🔥 1. Verifique se o Poetry já está instalado

```bash
poetry --version
```

Se aparecer a versão → continue.\
Se der erro → instale:

para Windows:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

para Linux/Mac:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

atualize se necessário:

```bash
poetry self update
```

---

# 📂 2. Criar o projeto (comandos rápidos)

1. Crie/clone o diretório do projeto

```bash
mkdir backend-template && cd backend-template
git init
```

2. Inicializar pyproject com Poetry (responda ou use --no-interaction)

```bash
poetry init --no-interaction
```

3. Instalar dependências base

```bash
poetry add django djangorestframework gunicorn dj-database-url python-dotenv whitenoise psycopg2-binary
```

4. Instalar dev-deps (formatadores, linters, test runner)

```bash
poetry add --group dev \
    "black>=25.11.0,<26.0.0" \
    "isort>=7.0.0,<8.0.0" \
    "flake8>=7.3.0,<8.0.0" \
    "flake8-isort>=7.0.0,<8.0.0" \
    "flake8-black>=0.4.0,<0.5.0" \
    pytest pytest-django
```

5. Criar projeto Django

```bash
poetry run django-admin startproject core .
```

6. Criar app exemplo

```bash
poetry run python manage.py startapp api
```

7. Rodar migrações iniciais

```bash
poetry run python manage.py migrate
```

---

# ⚙️ 3. pyproject.toml exemplo

```toml
[project]
name = "book-store"
version = "0.1.0"
description = "Book Store API"
authors = [{name = "Renato Minoita", email = "email@exemplo.com"}]
readme = "README.md"
requires-python = ">=3.11,<4.0"

[build-system]
requires = ["poetry-core>=1.5.0"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 120

[tool.isort]
profile = "black"
line_length = 120

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "core.settings"
python_files = "tests.py test_*.py *_tests.py"
pythonpath = "."

[dependency-groups]
dev = [
    "black (>=25.11.0,<26.0.0)",
    "isort (>=7.0.0,<8.0.0)",
    "flake8 (>=7.3.0,<8.0.0)",
    "flake8-isort (>=7.0.0,<8.0.0)",
    "flake8-black (>=0.4.0,<0.5.0)",
    "pytest",
    "pytest-django"
]
```

---

# ⚙️ 4. Configuração básica do Django

```python
import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
DEBUG = os.getenv("DEBUG", "1") == "1"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS",
                          "127.0.0.1 localhost").split()

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "rest_framework",

    # local
    "api",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database via DATABASE_URL (works com SQLite em dev e Postgres em prod)
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# Django REST Framework - paginação + configurações úteis
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    # authentication classes, throttling, etc. Você pode adicionar aqui.
}

```

---

# ⚙️ 5. Unificar todas as URLs no core

1. core/urls.py (unificação)

```python
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]


```

---

# ⚙️ 6. Exemplos de view / serializer / model (rápido)

1. api/models.py

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)

```

2. api/serializers.py

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

```

3. api/views.py

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

```

---

# ⚙️ 7. Configurar Black / isort / Flake8 (arquivos)

1. .flake8

```text
[flake8]
max-line-length = 120
extend-ignore = E203, W503
select = B,C,E,F,W,T4,B9
```

2. .pre-commit-config.yaml (opcional, muito útil)

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.11.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://gitlab.com/pycqa/flake8
    rev: 7.3.0
    hooks:
      - id: flake8
```

3. adicionar ao final do pyproject.toml

```toml
# Configurações de ferramentas
[tool.black]
line-length = 120

[tool.isort]
profile = "black"
line_length = 120

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "core.settings"
python_files = "tests.py test_*.py *_tests.py"
pythonpath = "."
```

---

# ⚙️ 8. Makefile

```makefile
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
```

---

# ⚙️ 9. Dockerfile e docker-compose (dev) + Render

1. Dockerfile (prod-ready)

```Dockerfile
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=core.settings
ENV PORT=8000

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
```

2. docker-compose.yml (dev)

```yaml
version: "3.9"
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: book_store
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env.dev
    depends_on:
      - db

volumes:
  postgres_data:
```

# ⚙️ 10. Deploy no Render

1. Exemplo render.yaml

```yaml
services:
  - type: web
    name: backend-django
    env: docker
    dockerfilePath: ./Dockerfile
    plan: free
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "0"
      - key: DJANGO_ALLOWED_HOSTS
        value: backend-django.onrender.com
databases:
  - name: db
    plan: free
```

---

# ⚙️ 11. GitHub Actions (CI) - workflow pronto

1. Crie .github/workflows/django-ci.yml

```yaml
name: Django CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: 1. Checkout Repository
        uses: actions/checkout@v4

      - name: 2. Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: 3. Install Poetry
        run: pip install poetry

      - name: 4. Configure Poetry
        run: poetry config virtualenvs.create false

      - name: 5. Install Dependencies
        run: poetry install --no-root -v

      - name: 6. Run Linters
        run: |
          poetry run black . --check
          poetry run isort . --check-only
          poetry run flake8 .

      - name: 7. Run Tests
        env:
          PYTHONPATH: "."
          SQL_ENGINE: django.db.backends.postgresql
          SQL_DATABASE: test_db
          SQL_USER: test_user
          SQL_PASSWORD: test_password
          SQL_HOST: localhost
          SQL_PORT: 5432
          SECRET_KEY: a-test-secret-key-for-ci
          DEBUG: "1"
        run: poetry run python manage.py test
```

---

# ⚙️ 12. .gitignore

```bash
# ============================================
# 🐍 PYTHON
# ============================================
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
env/
venv/

# Poetry
.poetry/
poetry.lock

# Byte-compiled / optimized / DLL files
*.pyd
*.pyo
*.so

# Distribution / packaging
build/
develop-eggs/
dist/
eggs/
.eggs/
parts/
*.egg-info/
.installed.cfg

# Installer logs
pip-log.txt
pip-delete-this-directory.txt


# ============================================
# 🧪 TESTS
# ============================================
.coverage
htmlcov/
coverage.xml
.pytest_cache/


# ============================================
# 📦 DJANGO / DRF
# ============================================
# Django cache
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Media / static (geradas automaticamente)
media/
staticfiles/
static/

# Gunicorn / Uvicorn logs
gunicorn*
uvicorn*


# ============================================
# 🧰 EDITOR & SO
# ============================================
# VSCode
.vscode/
.code-workspace

# MacOS
.DS_Store

# Windows
Thumbs.db


# ============================================
# 🔐 SECURITY (SUPER IMPORTANTE)
# ============================================
.env
.env.*
!.env.example

# Prevent secrets
secrets.json


# ============================================
# 🐳 DOCKER
# ============================================
# Somente arquivos gerados
docker-data/
```

---

# 🐳 13. .dockerignore

```bash
# ============================================
# 📦 DEPENDÊNCIAS & AMBIENTES
# ============================================
__pycache__/
*.py[cod]
*.pyd
*.pyo
*.so

# Virtual environments
.venv/
venv/
env/

# Poetry configs (exceto pyproject)
poetry.lock
.poetry/


# ============================================
# 🧰 EDITORES & SISTEMA
# ============================================
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db


# ============================================
# 📁 ARQUIVOS NÃO NECESSÁRIOS NO BUILD
# ============================================
tests/
docs/
media/
staticfiles/
static/
node_modules/

# Git
.git/
.gitignore


# ============================================
# 🔐 ARQUIVOS SENSÍVEIS
# ============================================
.env
.env.*
secrets.json


# ============================================
# 🛠 OUTROS
# ============================================
docker-compose.yml
```

---

# ⚙️ 14. requirements.txt para deploy (export)

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

---

# 🚀 15. Pushing para o GitHub

```bash
git add .
git commit -m "Initial project skeleton with Docker, Render, CI and QA tools"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/nome-repo.git
git push -u origin main

```

# 🎉 16. Seu projeto está pronto!

---

---

---

---

# 📘 Guia Completo — Comandos Essenciais para Docker, Poetry, Django, DRF e PostgreSQL

# 🚀 1. Docker — Comandos Essenciais

## 🟦 Containers

| Comando               | Descrição                 |
| --------------------- | ------------------------- |
| `docker ps`           | listar containers rodando |
| `docker ps -a`        | listar todos containers   |
| `docker stop <id>`    | parar container           |
| `docker start <id>`   | iniciar container         |
| `docker restart <id>` | reiniciar container       |
| `docker rm <id>`      | remover container parado  |
| `docker rm -f <id>`   | forçar remoção            |

## 🟦 Imagens

| Comando                  | Descrição        |
| ------------------------ | ---------------- |
| `docker images`          | listar imagens   |
| `docker rmi <imagem>`    | remover imagem   |
| `docker rmi -f <imagem>` | remover forçando |

## 🟦 Construir & Rodar

| Comando                           | Descrição       |
| --------------------------------- | --------------- |
| `docker build -t backend .`       | build da imagem |
| `docker run -p 8000:8000 backend` | executar imagem |

## 🟦 Logs + Debug

| Comando                            | Descrição           |
| ---------------------------------- | ------------------- |
| `docker logs -f <container>`       | logs em tempo real  |
| `docker exec -it <container> bash` | entrar no container |

## 🟦 Docker Compose

| Comando                        | Descrição            |
| ------------------------------ | -------------------- |
| `docker-compose up -d`         | subir tudo           |
| `docker-compose up --build`    | rebuild + subir      |
| `docker-compose down`          | parar e remover      |
| `docker-compose logs -f`       | logs dos serviços    |
| `docker-compose exec web bash` | shell no serviço web |

---

# 🐍 2. Poetry — Comandos Modernos (2025)

## 🟪 Projeto & Ambiente

| Comando               | Descrição             |
| --------------------- | --------------------- |
| `poetry new backend`  | criar projeto         |
| `poetry install`      | instalar dependências |
| `poetry env activate` | ativar ambiente       |

## 🟪 Dependências

| Comando                                      | Descrição          |
| -------------------------------------------- | ------------------ |
| `poetry add django`                          | adicionar Django   |
| `poetry add djangorestframework`             | adicionar DRF      |
| `poetry add psycopg[binary]`                 | driver PostgreSQL  |
| `poetry add --dev black isort flake8 pytest` | ferramentas de dev |

## 🟪 Gerenciar Pacotes

| Comando                | Descrição      |
| ---------------------- | -------------- |
| `poetry remove pacote` | remover pacote |

## 🟪 Executar Comandos

| Comando                                 | Descrição      |
| --------------------------------------- | -------------- |
| `poetry run python manage.py runserver` | rodar servidor |
| `poetry run pytest`                     | rodar testes   |

## 🟪 Exportar requirements

| Comando                                                       | Descrição              |
| ------------------------------------------------------------- | ---------------------- |
| `poetry export -f requirements.txt --output requirements.txt` | gerar requirements.txt |

---

# 🐍 3. Django / DRF — Comandos Essenciais

## 🟩 Criar Projeto e Apps

| Comando                                       | Descrição     |
| --------------------------------------------- | ------------- |
| `poetry run django-admin startproject core .` | criar projeto |
| `poetry run python manage.py startapp api`    | criar app     |

## 🟩 Migrações

| Comando                                      | Descrição         |
| -------------------------------------------- | ----------------- |
| `poetry run python manage.py makemigrations` | gerar migrações   |
| `poetry run python manage.py migrate`        | aplicar migrações |

## 🟩 Usuário e Server

| Comando                                       | Descrição         |
| --------------------------------------------- | ----------------- |
| `poetry run python manage.py createsuperuser` | criar superuser   |
| `poetry run python manage.py runserver`       | rodar servidor    |
| `poetry run python manage.py collectstatic`   | coletar estáticos |
| `poetry run python manage.py shell`           | abrir shell       |

---

# 🧹 4. Qualidade de Código (Black, Isort, Flake8)

| Comando              | Descrição         |
| -------------------- | ----------------- |
| `poetry run black .` | formatar código   |
| `poetry run isort .` | organizar imports |
| `poetry run flake8`  | analisar erros    |

---

# 🧪 5. Pytest — Testes

| Comando                   | Descrição           |
| ------------------------- | ------------------- |
| `poetry run pytest`       | rodar testes        |
| `poetry run pytest --cov` | rodar com cobertura |

---

# 🐳 + 🐍 6. Docker + Django (Ambiente Integrado)

| Comando                                                           | Descrição             |
| ----------------------------------------------------------------- | --------------------- |
| `docker-compose up --build`                                       | build + subir         |
| `docker-compose exec web bash`                                    | entrar no container   |
| `docker-compose exec web python manage.py migrate`                | migrations via Docker |
| `docker-compose exec web python manage.py runserver 0.0.0.0:8000` | rodar server          |

---

# 🐘 7. PostgreSQL (Docker)

## 🟦 Acessar Banco

| Comando                                                    | Descrição       |
| ---------------------------------------------------------- | --------------- |
| `docker-compose exec db psql -U postgres -d nome_do_banco` | entrar no banco |

## 🟦 Dentro do PSQL

| Comando | Descrição      |
| ------- | -------------- |
| `\l`    | listar bancos  |
| `\dt`   | listar tabelas |

---

# 🌐 8. Render — Deploy

Render não usa CLI, mas aqui vão comandos úteis:

| Comando                                             | Descrição       |
| --------------------------------------------------- | --------------- |
| `render logs <serviço>`                             | visualizar logs |
| `curl https://SEU_BACKEND.onrender.com/api/health/` | healthcheck     |

---

# ⚙️ 9. Makefile (opcional)

Se quiser, posso gerar um Makefile automático com comandos:

- `make run`
- `make format`
- `make lint`
- `make build`
- `make docker`
- `make deploy`

# 👤 Autor

Feito com 💙 por [Renato Minoita](https://www.linkedin.com/in/renato-minoita/)

Confira mais no [GitHub](https://github.com/RNT13)
