# ==============================================================================
# Makefile - C216 (Sistemas Distribuídos)
# ==============================================================================

# ------------------------------------------------------------------------------
# Variáveis
# ------------------------------------------------------------------------------
PYTHON      := python
POETRY      := poetry
BACKEND_DIR := backend
HOST        := 0.0.0.0
PORT        := 8000

# ------------------------------------------------------------------------------
# Declaração de Alvos .PHONY
# ------------------------------------------------------------------------------
.PHONY: help install run test clean lock

# Alvo padrão executado ao rodar apenas 'make'
.DEFAULT_GOAL := help

# ------------------------------------------------------------------------------
# Comandos e Regras
# ------------------------------------------------------------------------------

## help: Exibe esta mensagem de ajuda com todos os comandos disponíveis
help:
	@echo "======================================================================"
	@echo "  COMANDOS DISPONIVEIS NO PROJETO - C216 (SISTEMAS DISTRIBUIDOS)"
	@echo "======================================================================"
	@echo "  make help       - Exibe este menu de ajuda"
	@echo "  make install    - Instala as dependencias do backend com Poetry"
	@echo "  make run        - Inicia a API FastAPI (Uvicorn) com hot-reload"
	@echo "  make test       - Executa os testes automatizados com Pytest"
	@echo "  make lock       - Gera/atualiza o arquivo poetry.lock"
	@echo "  make clean      - Remove arquivos de cache e temporarios"
	@echo "======================================================================"

## install: Instala todas as dependências do projeto via Poetry
install:
	cd $(BACKEND_DIR) && $(POETRY) install

## run: Executa o servidor FastAPI localmente
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
