# Backend - C216 (Sistemas Distribuídos)

Backend em Python com FastAPI com arquitetura modular, gerenciado via Poetry, conteinerizado com Docker e com pipeline de Integração Contínua (CI) via GitHub Actions.

## Arquitetura do Projeto
- `main.py`: Ponto de entrada da aplicação, responsável exclusivamente pela inicialização do FastAPI e inclusão dos roteadores.
- `schemas/`: Modelos de dados e validações com Pydantic (`item.py`).
- `services/`: Regras de negócio e camada de manipulação de dados (`item_service.py`).
- `routers/`: Controladores e endpoints da API organizados por contexto:
  - `items.py`: Rotas do recurso com suporte completo a GET, POST, PUT, PATCH e DELETE, com uso de Path e Query Parameters.
  - `system.py`: Rotas de status do sistema (`/`, `/health`, `/db-status`).
- `tests/`: Separação explícita da suíte de testes:
  - `unit/`: Testes unitários focados nas regras de negócio da camada de serviço.
  - `integration/`: Testes de integração via `TestClient` cobrindo todos os endpoints HTTP, parâmetros e validações.
  - `conftest.py`: Fixtures compartilhadas do Pytest.

## Como Executar os Testes

### 1. Pelo Makefile (na raiz do projeto)
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

### 2. Diretamente com o Poetry (dentro de `backend`)
```bash
cd backend
poetry run pytest tests/ -v
```

### 3. Execução em CI (GitHub Actions)
Os testes são executados automaticamente a cada `push` e `pull_request` no GitHub através do workflow `.github/workflows/ci-backend.yml`.

## Como Executar a Aplicação

### Via Docker Compose
```bash
make compose-up
```

### Desenvolvimento Local (Host)
```bash
make install
make run
```
