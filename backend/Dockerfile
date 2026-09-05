# Imagem base oficial do Python (versão slim para manter a imagem leve e segura)
FROM python:3.11-slim

# Variáveis de ambiente para execução otimizada do Python e Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

# Instala curl necessário para baixar o Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalação do Poetry usando o instalador oficial
RUN curl -sSL https://install.python-poetry.org | python3 -

# Define o diretório de trabalho na imagem
WORKDIR /app

# Copia primeiro apenas os manifestos de dependência para aproveitar o cache de camadas do Docker
COPY pyproject.toml poetry.lock* /app/

# Instala as dependências de produção sem criar virtualenv (já isolado no container)
RUN poetry install --no-interaction --no-ansi --no-root

# Copia todo o código-fonte restante da aplicação
COPY . /app/

# Expõe a porta 8000 do serviço
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn escutando em todas as interfaces de rede
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
