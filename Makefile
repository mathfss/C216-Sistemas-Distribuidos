PYTHON            := python
POETRY            := poetry
BACKEND_DIR       := backend
FRONTEND_DIR      := frontend
NPM               := npm
HOST              := 0.0.0.0
PORT              := 8000

DOCKER            := docker
DOCKER_COMPOSE    := docker compose
IMAGE_NAME        := c216-backend
COMPOSE_FILE      := compose.yml
DB_CONTAINER      := c216_db
BACKEND_CONTAINER := c216_backend

.PHONY: help install run test test-unit test-integration lock clean \
        lint format db-upgrade db-migration db-current \
        frontend-install frontend-dev frontend-lint frontend-format \
        frontend-check frontend-test frontend-test-e2e frontend-build \
        check-all e2e \
        docker-build compose-up compose-down compose-logs \
        compose-ps compose-restart up-build logs-api backend-shell db-shell

.DEFAULT_GOAL := help

help:
	@echo "Comandos disponiveis:"
	@echo "  make install            - Instala dependencias com poetry"
	@echo "  make run                - Roda o backend localmente"
	@echo "  make test               - Roda todos os testes do backend"
	@echo "  make test-unit          - Roda apenas os testes unitarios do backend"
	@echo "  make test-integration   - Roda apenas os testes de integracao do backend"
	@echo "  make lint               - Executa o linter ruff no backend"
	@echo "  make format             - Formata o codigo com ruff"
	@echo "  make db-upgrade         - Executa as migrations com alembic (upgrade head)"
	@echo "  make db-migration       - Cria uma nova migration (uso: make db-migration msg=\"nome\")"
	@echo "  make db-current         - Exibe a revisao atual da migration do banco"
	@echo "  make frontend-install   - Instala dependencias do frontend com npm ci"
	@echo "  make frontend-dev       - Inicia o servidor de desenvolvimento Vite"
	@echo "  make frontend-lint      - Executa biome lint no frontend"
	@echo "  make frontend-format    - Formata o codigo do frontend com biome"
	@echo "  make frontend-check     - Valida lint e formatacao do frontend sem alterar"
	@echo "  make frontend-test      - Executa os testes do frontend com Vitest"
	@echo "  make frontend-test-e2e  - Executa os testes E2E com Playwright"
	@echo "  make frontend-build     - Gera o build de producao do frontend"
	@echo "  make e2e                - Executa E2E full-stack em stack isolada Docker (lab-e2e)"
	@echo "  make check-all          - Executa todas as verificacoes (backend + frontend + e2e)"
	@echo "  make lock               - Atualiza o poetry.lock"
	@echo "  make clean              - Limpa arquivos de cache"
	@echo "  make docker-build       - Build da imagem docker do backend"
	@echo "  make compose-up         - Sobe os containers (backend e banco)"
	@echo "  make compose-down       - Para os containers"
	@echo "  make compose-logs       - Mostra os logs dos containers"
	@echo "  make compose-ps         - Status dos containers"
	@echo "  make compose-restart    - Reinicia os containers"
	@echo "  make up-build           - Alias para subir containers recriando imagens"
	@echo "  make logs-api           - Alias para ver logs do container"
	@echo "  make backend-shell      - Abre terminal no container do backend"
	@echo "  make db-shell           - Entra no psql do postgres"

install:
	cd $(BACKEND_DIR) && $(POETRY) install

run:
	cd $(BACKEND_DIR) && $(POETRY) run uvicorn main:app --host $(HOST) --port $(PORT) --reload

test:
	cd $(BACKEND_DIR) && $(POETRY) run pytest tests/ -v

test-unit:
	cd $(BACKEND_DIR) && $(POETRY) run pytest tests/unit/ -v

test-integration:
	cd $(BACKEND_DIR) && $(POETRY) run pytest tests/integration/ -v

lint:
	cd $(BACKEND_DIR) && $(POETRY) run ruff check .

format:
	cd $(BACKEND_DIR) && $(POETRY) run ruff format .

db-upgrade:
	cd $(BACKEND_DIR) && $(POETRY) run alembic upgrade head

db-migration:
	cd $(BACKEND_DIR) && $(POETRY) run alembic revision --autogenerate -m "$(msg)"

db-current:
	cd $(BACKEND_DIR) && $(POETRY) run alembic current

frontend-install:
	$(NPM) --prefix $(FRONTEND_DIR) ci

frontend-dev:
	$(NPM) --prefix $(FRONTEND_DIR) run dev

frontend-lint:
	$(NPM) --prefix $(FRONTEND_DIR) run lint

frontend-format:
	$(NPM) --prefix $(FRONTEND_DIR) run format

frontend-check:
	$(NPM) --prefix $(FRONTEND_DIR) run check

frontend-test:
	$(NPM) --prefix $(FRONTEND_DIR) run test

frontend-test-e2e:
	$(NPM) --prefix $(FRONTEND_DIR) run test:e2e

frontend-build:
	$(NPM) --prefix $(FRONTEND_DIR) run build

e2e:
	API_PORT=8001 FRONTEND_PORT=5174 VITE_API_URL=http://localhost:8001 CORS_ORIGINS=http://localhost:5174,http://127.0.0.1:5174 $(DOCKER_COMPOSE) -p lab-e2e -f $(COMPOSE_FILE) up -d --build --wait
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do curl -sf http://localhost:5174 > /dev/null 2>&1 && break || sleep 1; done
	E2E_BASE_URL=http://localhost:5174 $(NPM) --prefix $(FRONTEND_DIR) run test:e2e; \
	STATUS=$$?; \
	$(DOCKER_COMPOSE) -p lab-e2e -f $(COMPOSE_FILE) down -v; \
	exit $$STATUS

check-all: lint test frontend-check frontend-test frontend-build e2e

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

up-build: compose-up

compose-down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

compose-logs:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f

logs-api: compose-logs

compose-ps:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps

compose-restart:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) restart

backend-shell:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec api sh

db-shell:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec db psql -U postgres -d c216_db
