# Usar uma imagem oficial do Python 3.12
FROM python:3.12

# Criar diretório de trabalho
WORKDIR /

# Copiar arquivos do projeto para dentro do container
COPY . /

# Instalar Poetry
RUN pip install poetry

RUN poetry run python manage.py collectstatic --noinput

# Instalar dependências do projeto
RUN export $(grep -v '^#' .env | xargs) && \
    poetry install --no-root

RUN poetry run python manage.py migrate

# Comando para rodar o app (mude conforme necessário)
# CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD poetry run python create_superuser.py || true && poetry run gunicorn --bind 0.0.0.0:8000 core.wsgi:application