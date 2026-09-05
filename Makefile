# ==============================================================================
# Makefile - C216 (Sistemas Distribuídos)
# Prática 1 + Prática 2: Poetry, FastAPI, Docker & Docker Compose
# ==============================================================================

# ------------------------------------------------------------------------------
# Variáveis de Configuração do Ambiente e Aplicação
# ------------------------------------------------------------------------------
PYTHON            := python
POETRY            := poetry
BACKEND_DIR       := backend
HOST              := 0.0.0.0
PORT              := 8000

# ------------------------------------------------------------------------------
# Variáveis do Docker e Orquestração
# ------------------------------------------------------------------------------
DOCKER            := docker
DOCKER_COMPOSE    := docker compose
IMAGE_NAME        := c216-backend
COMPOSE_FILE      := docker-compose.yml
DB_CONTAINER      := c216_db
BACKEND_CONTAINER := c216_backend

# ------------------------------------------------------------------------------
# Declaração de Alvos .PHONY (Evita conflito com arquivos de mesmo nome)
# ------------------------------------------------------------------------------
.PHONY: help install run test lock clean \
        docker-build compose-up compose-down compose-logs \
        compose-ps compose-restart backend-shell db-shell

# Alvo padrão executado ao rodar apenas 'make'
.DEFAULT_GOAL := help

# ==============================================================================
# Comandos e Regras
# ==============================================================================

## help: Exibe esta mensagem de ajuda com todos os comandos disponíveis
help:
	@echo "======================================================================"
	@echo "  COMANDOS DISPONIVEIS NO PROJETO - C216 (SISTEMAS DISTRIBUIDOS)"
	@echo "======================================================================"
	@echo "  --- Desenvolvimento Local (Prática 1) ---"
	@echo "  make help            - Exibe este menu de ajuda"
	@echo "  make install         - Instala as dependencias do backend via Poetry"
	@echo "  make run             - Inicia o servidor local FastAPI com Uvicorn"
	@echo "  make test            - Executa os testes automatizados com Pytest"
	@echo "  make lock            - Gera/atualiza o arquivo poetry.lock"
	@echo "  make clean           - Remove arquivos temporarios e cache do Python"
	@echo ""
	@echo "  --- Containers e Docker Compose (Prática 2) ---"
	@echo "  make docker-build    - Compila a imagem Docker do backend"
	@echo "  make compose-up      - Sobe todos os servicos (backend + db) em background"
	@echo "  make compose-down    - Para e remove todos os containers e redes"
	@echo "  make compose-logs    - Acompanha os logs em tempo real dos containers"
	@echo "  make compose-ps      - Lista o status e portas dos servicos ativos"
	@echo "  make compose-restart - Reinicia todos os servicos do Docker Compose"
	@echo "  make backend-shell   - Abre terminal interativo no container do backend"
	@echo "  make db-shell        - Abre console interativo (psql) no PostgreSQL"
	@echo "======================================================================"

# ------------------------------------------------------------------------------
# Comandos de Desenvolvimento Local
# ------------------------------------------------------------------------------

## install: Instala todas as dependências do projeto via Poetry
install:
	cd $(BACKEND_DIR) && $(POETRY) install

## run: Executa o servidor FastAPI localmente na máquina hospedeira
run:
	cd $(BACKEND_DIR) && $(POETRY) run uvicorn main:app --host $(HOST) --port $(PORT) --reload

## test: Executa a suíte de testes com Pytest
test:
	cd $(BACKEND_DIR) && $(POETRY) run pytest -v

## lock: Gera ou atualiza o lockfile de dependências
lock:
	cd $(BACKEND_DIR) && $(POETRY) lock

## clean: Remove arquivos de cache do Python e testes
clean:
	@echo "Limpando caches e arquivos temporarios..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# ------------------------------------------------------------------------------
# Comandos de Containers com Docker & Docker Compose (Prática 2)
# ------------------------------------------------------------------------------

## docker-build: Constrói a imagem Docker isolada para o serviço backend
docker-build:
	$(DOCKER) build -t $(IMAGE_NAME):latest ./$(BACKEND_DIR)

## compose-up: Constrói as imagens e inicia todos os serviços em background
compose-up:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d --build

## compose-down: Para e encerra a execução dos containers e da rede compartilhada
compose-down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

## compose-logs: Exibe e monitora logs de todos os containers simultaneamente
compose-logs:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f

## compose-ps: Exibe os containers em execução com status de integridade (healthcheck)
compose-ps:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps

## compose-restart: Reinicia os serviços do Docker Compose
compose-restart:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) restart

## backend-shell: Abre um terminal interativo dentro do container do backend
backend-shell:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(BACKEND_CONTAINER) sh

## db-shell: Acessa o cliente psql dentro do container do banco PostgreSQL
db-shell:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U postgres -d c216_db
