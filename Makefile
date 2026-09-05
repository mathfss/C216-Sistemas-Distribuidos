PYTHON            := python
POETRY            := poetry
BACKEND_DIR       := backend
HOST              := 0.0.0.0
PORT              := 8000

DOCKER            := docker
DOCKER_COMPOSE    := docker compose
IMAGE_NAME        := c216-backend
COMPOSE_FILE      := docker-compose.yml
DB_CONTAINER      := c216_db
BACKEND_CONTAINER := c216_backend

.PHONY: help install run test lock clean \
        docker-build compose-up compose-down compose-logs \
        compose-ps compose-restart backend-shell db-shell

.DEFAULT_GOAL := help

help:
	@echo "Comandos disponiveis:"
	@echo "  make install         - Instala dependencias com poetry"
	@echo "  make run             - Roda o backend localmente"
	@echo "  make test            - Roda os testes com pytest"
	@echo "  make lock            - Atualiza o poetry.lock"
	@echo "  make clean           - Limpa arquivos de cache"
	@echo "  make docker-build    - Build da imagem docker do backend"
	@echo "  make compose-up      - Sobe os containers (backend e banco)"
	@echo "  make compose-down    - Para os containers"
	@echo "  make compose-logs    - Mostra os logs dos containers"
	@echo "  make compose-ps      - Status dos containers"
	@echo "  make compose-restart - Reinicia os containers"
	@echo "  make backend-shell   - Abre terminal no container do backend"
	@echo "  make db-shell        - Entra no psql do postgres"

install:
	cd $(BACKEND_DIR) && $(POETRY) install

run:
	cd $(BACKEND_DIR) && $(POETRY) run uvicorn main:app --host $(HOST) --port $(PORT) --reload

test:
	cd $(BACKEND_DIR) && $(POETRY) run pytest -v

lock:
	cd $(BACKEND_DIR) && $(POETRY) lock

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

docker-build:
	$(DOCKER) build -t $(IMAGE_NAME):latest ./$(BACKEND_DIR)

compose-up:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d --build

compose-down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

compose-logs:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f

compose-ps:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps

compose-restart:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) restart

backend-shell:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(BACKEND_CONTAINER) sh

db-shell:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U postgres -d c216_db
