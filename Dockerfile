# Base image
FROM python:3.10-buster

# 1. Diretório de trabalho
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY [ "requirements.txt", "docker-entrypoint.sh", "./"]
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && chmod +x ./docker-entrypoint.sh

# copy project
COPY . .

# 4. Expõe porta da API (UVicorn) e da Flower, se desejar
EXPOSE 8000 5555

# 5. Entry point
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# 6. Processo padrão (substituível no docker-compose)
CMD ["/app/docker-entrypoint.sh", "api"]