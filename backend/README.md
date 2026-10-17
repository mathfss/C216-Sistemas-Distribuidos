# Backend - C216 (Sistemas Distribuídos)

Backend em Python com FastAPI integrado a persistência relacional com PostgreSQL, SQLAlchemy ORM e migrations com Alembic, organizado em arquitetura em camadas.

## Arquitetura do Projeto
- `app/`: Pacote principal da aplicação.
  - `main.py`: Inicialização do FastAPI e inclusão das rotas.
  - `api/routes/`: Controladores e endpoints da API (`items.py`, `system.py`).
  - `schemas/`: Schemas Pydantic para validação de entrada e saída da API (`item.py`).
  - `services/`: Regras de negócio intermediando rotas e repositórios (`item_service.py`).
  - `repositories/`: Camada de persistência e acesso a dados via SQLAlchemy (`item_repository.py`).
  - `models/`: Modelos ORM mapeados para tabelas do PostgreSQL (`item.py`).
  - `database/`: Configuração da engine, sessões (`session.py`) e classe declarativa `Base` (`base.py`).
  - `core/`: Configurações centralizadas e leitura de variáveis de ambiente (`config.py`).
- `alembic/`: Gerenciamento e versionamento de migrations de banco de dados.
- `tests/`: Suíte de testes automatizados com Pytest.
  - `unit/`: Testes unitários das regras de negócio e camada de serviço.
  - `integration/`: Testes de integração dos endpoints via TestClient.
  - `conftest.py`: Fixtures de banco de teste e cliente HTTP.

## Como Executar as Migrations

- Aplicar migrations pendentes:
  ```bash
  make db-upgrade
  ```
- Gerar nova migration baseada nos modelos:
  ```bash
  make db-migration msg="descricao_da_mudanca"
  ```
- Verificar a revisão atual do banco:
  ```bash
  make db-current
  ```

## Como Executar os Testes

- Todos os testes (unitários + integração):
  ```bash
  make test
  ```
- Apenas testes unitários:
  ```bash
  make test-unit
  ```
- Apenas testes de integração:
  ```bash
  make test-integration
  ```

## Lint e Formatação

- Verificar código com linter:
  ```bash
  make lint
  ```
- Formatar código automaticamente:
  ```bash
  make format
  ```

## Como Executar a Aplicação

- Via Docker Compose (API + PostgreSQL):
  ```bash
  make compose-up
  ```
- Desenvolvimento local:
  ```bash
  make install
  make run
  ```
