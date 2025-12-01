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
poetry add django djangorestframework gunicorn dj-database-url python-dotenv whitenoise psycopg2-binary pillow factory_boy django-cors-headers djangorestframework-simplejwt drf-spectacular drf-spectacular-sidecar
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

# ⚙️ 3. criação do .env

```bash
# ================================
# 🔐 DJANGO SETTINGS
# ================================
SECRET_KEY=coloque_uma_chave_muito_grande_e_aleatoria_aqui
DEBUG=0

# Lista de domínios permitidos
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# CSRF previne ataques que usam a sessão do usuário sem permissão.
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://127.0.0.1:8000


# ================================
# 🗄️ DATABASE (POSTGRES)
# ================================
POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario_do_banco
POSTGRES_PASSWORD=senha_forte_aqui

DATABASE_HOST=postgres
DATABASE_PORT=5432


# ================================
# 🌐 CORS / FRONTEND
# ================================
CORS_ALLOWED_ORIGINS=https://seu-frontend.com
CORS_ALLOW_CREDENTIALS=True


# ================================
# 📨 E-MAIL (envio online)
# ================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seuemail@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app


# ================================
# 🔥 LOG LEVEL (produção)
# ================================
DJANGO_LOG_LEVEL=INFO

DRF_RENDERER_DEFAULT=JSON
```

---

# ⚙️ 4. pyproject.toml exemplo

```toml
[project]
name = "rnt-hub"
version = "0.1.0"
description = "Projeto final da EBAC"
authors = [
    {name = "RNT13",email = "renatornt13@gmail.com"}
]
readme = "README.md"
requires-python = ">=3.13,<4.0"
dependencies = [
    "django (>=5.2.8,<6.0.0)",
    "djangorestframework (>=3.16.1,<4.0.0)",
    "gunicorn (>=23.0.0,<24.0.0)",
    "psycopg2-binary (>=2.9.11,<3.0.0)",
    "dj-database-url (>=3.0.1,<4.0.0)",
    "python-dotenv (>=1.2.1,<2.0.0)",
    "whitenoise (>=6.11.0,<7.0.0)",
    "pillow (>=12.0.0,<13.0.0)",
    "django-cors-headers (>=4.9.0,<5.0.0)"
]

[tool.poetry]
package-mode = false

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

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

[dependency-groups]
dev = [
    "black (>=25.11.0,<26.0.0)",
    "isort (>=7.0.0,<8.0.0)",
    "flake8 (>=7.3.0,<8.0.0)",
    "flake8-isort (>=7.0.0,<8.0.0)",
    "flake8-black (>=0.4.0,<0.5.0)",
    "factory-boy (>=3.3.3,<4.0.0)"
]

```

---

# ⚙️ 5. Configuração básica do Django

```python
import os
from pathlib import Path
from datetime import timedelta

import dj_database_url
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
DEBUG = os.getenv("DEBUG", "1") == "1"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin
]

AUTH_USER_MODEL = "users.User"

# --------------------------------------------------------------------
# Apps
# --------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # locais
    "accounts",
    "posts",
    "comments",
    "likes",
    "follows",
    "notifications",
    "feed",
]

# --------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "core.urls"

# ----------------------------------------------------------------------
# CORS
# ----------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://rnt-hub.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_HEADERS = True

# --------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------
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

# --------------------------------------------------------------------
# Database
# --------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# --------------------------------------------------------------------
# Password validators
# --------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------
# Internacionalização
# --------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------
# Static files
# --------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------------------------
# Django REST Framework + JWT
# --------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# --------------------------------------------------------------------
# SIMPLE JWT
# --------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------------------------
# Swagger
# --------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "RNT-Hub API",
    "DESCRIPTION": "Documentação completa da API RNT-Hub",
    "VERSION": "1.0.0",
}

# Remover HTML Browsable API em produção
if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
    ]

# --------------------------------------------------------------------
# Segurança
# --------------------------------------------------------------------
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

```

---

# ⚙️ 6. core/urls.py

1. core/urls.py

```python
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # ---------------------------------------------------------
    # 📘 Documentação da API
    # ---------------------------------------------------------

    # Swagger UI (interface bonita e interativa)
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Arquivo JSON/YAML do schema gerado pelo DRF-Spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),

    # Redoc (documentação alternativa)
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # ---------------------------------------------------------
    # Admin
    # ---------------------------------------------------------
    path("admin/", admin.site.urls),

    # ---------------------------------------------------------
    # JWT Authentication
    # ---------------------------------------------------------
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ---------------------------------------------------------
    # Apps da API
    # ---------------------------------------------------------
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/posts/", include("posts.urls")),
    path("api/v1/likes/", include("likes.urls")),
    path("api/v1/follows/", include("follows.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/feed/", include("feed.urls")),
]
```

---

# ⚙️ 7. Exemplos de view / serializer / model (rápido)

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

4. api/urls.py

```python
from django.urls import path
from .views import BookViewSet

urlpatterns = [
    path("", BookViewSet.as_view({"get": "list"})),
    path("<int:pk>/", BookViewSet.as_view({"get": "retrieve"})),
]

```

---

# ⚙️ 8. Adicione testes ao projeto

1. api/tests.py

```bash
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse("books-list")

    def test_list_books(self):
        """Testa listar livros com paginação"""

        Book.objects.create(title="Livro 1", author="Autor 1", price=10.50)

        response = self.client.get(self.list_url)

        # Verifica status HTTP
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica estrutura da paginação
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)

        # Deve haver exatamente 1 livro
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_book(self):
        """Testa criar um livro via POST"""

        data = {"title": "Novo Livro", "author": "Autor X", "price": "25.90"}
        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().title, "Novo Livro")

    def test_retrieve_book(self):
        """Testa detalhe de um livro"""

        book = Book.objects.create(title="Livro A", author="Autor A", price=30.00)

        url = reverse("books-detail", args=[book.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Livro A")

    def test_update_book(self):
        """Testa atualizar um livro via PUT"""

        book = Book.objects.create(title="Original", author="Autor", price=50.00)

        url = reverse("books-detail", args=[book.id])
        data = {"title": "Atualizado", "author": "Autor", "price": "50.00"}

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Atualizado")

    def test_delete_book(self):
        """Testa deletar um livro"""

        book = Book.objects.create(title="AAA", author="BBB", price=10.00)

        url = reverse("books-detail", args=[book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
```

# ⚙️ 9. Configurar Black / isort / Flake8 (arquivos)

1. .flake8

```text
[flake8]
max-line-length = 120
extend-ignore = E203, W503
select = B,C,E,F,W,T4,B9

# Pastas e arquivos a ignorar
exclude =
    migrations,
    __pycache__,
    manage.py,
    env/,
    venv/,
    .venv/
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

# ⚙️ 10. Makefile

```makefile
SERVICE_NAME = web
# Use "docker-compose run --rm" para garantir que a virtualenv seja criada corretamente dentro do container
PYTHON_EXEC = docker-compose exec $(SERVICE_NAME) python

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
	$(PYTHON_EXEC) -m pytest

format: ## 🎨 Format code (black + isort)
	$(PYTHON_EXEC) -m black .
	$(PYTHON_EXEC) -m isort .

lint: ## 🧐 Lint (flake8 + checks)
	$(PYTHON_EXEC) -m flake8 .
	$(PYTHON_EXEC) -m black --check .
	$(PYTHON_EXEC) -m isort --check .

reset: ## 🔥 Reset docker environment (use carefully)
	docker-compose down -v
	docker system prune -a --volumes -f

```

---

# ⚙️ 11. Dockerfile e docker-compose (dev) + Render

1. Dockerfile (prod-ready)

```Dockerfile
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Dependências mínimas necessárias
RUN apt-get update && \
    apt-get install -y gcc libpq-dev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN pip install poetry

# Copia apenas pyproject/lock para cache
COPY pyproject.toml poetry.lock* /app/

# Ativa virtualenv dentro do container (mais leve no Render)
RUN poetry config virtualenvs.create true \
    && poetry install --no-root --no-interaction --no-ansi

COPY . /app

ENV DJANGO_SETTINGS_MODULE=core.settings

# Static files
RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "poetry run python manage.py migrate --noinput && poetry run gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 2 --timeout 120"]

```

2. docker-compose.yml (dev)

```yaml
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
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    environment:
      POETRY_VIRTUALENVS_IN_PROJECT: "false"
      POETRY_VIRTUALENVS_PATH: "/opt/venvs"

volumes:
  postgres_data:
```

# ⚙️ 12. Deploy no Render

1. Exemplo render.yaml

```yaml
services:
  - type: web
    name: Nome_do_projeto_aqui
    env: docker
    dockerfilePath: ./Dockerfile
    plan: free
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "0"
      - key: DJANGO_ALLOWED_HOSTS
        value: Nome_do_projeto_aqui.onrender.com
databases:
  - name: db
    plan: free
```

---

# ⚙️ 13. GitHub Actions (CI) - workflow pronto

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
          --health-cmd "pg_isready"
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

      - name: Wait for Postgres
        run: |
          for i in {1..10}; do
            pg_isready -h localhost -p 5432 && break
            echo "Waiting for Postgres..."
            sleep 3
          done

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

# ⚙️ 14. .gitignore

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

# 🐳 15. .dockerignore

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

# ⚙️ 16. requirements.txt para deploy (export)

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

ou

```bash
pip freeze > requirements.txt
```

---

# 🚀 17. Pushing para o GitHub

```bash
git add .
git commit -m "Initial project skeleton with Docker, Render, CI and QA tools"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/nome-repo.git
git push -u origin main

```

# 🎉 18. Seu projeto está pronto!

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

| Comando                                                                  | Descrição              |
| ------------------------------------------------------------------------ | ---------------------- |
| `poetry export -f requirements.txt -o requirements.txt --without-hashes` | gerar requirements.txt |

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

# ⚙️ 9. Makefile base do Projeto

| Comando                | Descrição                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `make help`            | Mostra todos os comandos disponíveis no Makefile                                                                               |
| `make up`              | Builda e sobe os containers Docker em background (`docker-compose up -d --build`)                                              |
| `make down`            | Para e remove os containers Docker (`docker-compose down`)                                                                     |
| `make logs`            | Mostra os logs em tempo real dos containers (`docker-compose logs -f`)                                                         |
| `make shell`           | Abre um shell no container `web` (`docker-compose exec web /bin/sh`)                                                           |
| `make migrate`         | Cria migrações e aplica no banco de dados (`poetry run python manage.py makemigrations` e `migrate`)                           |
| `make createsuperuser` | Cria um superuser interativo no Django (`poetry run python manage.py createsuperuser`)                                         |
| `make collectstatic`   | Coleta arquivos estáticos (`poetry run python manage.py collectstatic --noinput`)                                              |
| `make test`            | Roda os testes usando pytest (`docker-compose exec web poetry run pytest`)                                                     |
| `make format`          | Formata o código com Black e organiza imports com Isort (`docker-compose exec web poetry run black .` e `isort .`)             |
| `make lint`            | Checa o código com Flake8, Black e Isort (`docker-compose exec web poetry run flake8 .`, `black --check .`, `isort --check .`) |
| `make reset`           | Reseta todo o ambiente Docker (remove containers, volumes, imagens e cache)                                                    |

---

# 👤 Autor

Feito com 💙 por [Renato Minoita](https://www.linkedin.com/in/renato-minoita/)

Confira mais no [GitHub](https://github.com/RNT13)
