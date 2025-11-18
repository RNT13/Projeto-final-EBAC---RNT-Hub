FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Dependências do sistema
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copia apenas pyproject e poetry.lock para cache
COPY pyproject.toml poetry.lock* /app/

# Configura Poetry para não criar virtualenvs e instala dependências no container
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copia o restante do projeto
COPY . /app

ENV DJANGO_SETTINGS_MODULE=core.settings
ENV PORT=8000

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando padrão
CMD ["bash", "-c", "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]
