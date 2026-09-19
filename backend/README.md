# Backend - C216 (Sistemas Distribuídos)

Backend em Python com FastAPI, gerenciado via Poetry, conteinerizado com Docker e com pipeline de Integração Contínua (CI) via GitHub Actions.

## Estrutura de Diretórios
- `main.py`: Aplicação FastAPI e rotas da API.
- `tests/`: Suíte de testes automatizados com Pytest.
  - `conftest.py`: Fixtures de teste reutilizáveis (`client`, `sample_item_payload`, `reset_database`).
  - `test_api.py`: Testes unitários cobrindo rotas, validações, casos de erro e parametrização.
- `Dockerfile` e `.dockerignore`: Definições para criação da imagem do container.
- `pyproject.toml` e `poetry.lock`: Gerenciamento de dependências.

## Como Executar os Testes

### 1. Pelo Makefile (na raiz do projeto)
```bash
make test
```

### 2. Diretamente com o Poetry (dentro da pasta `backend`)
```bash
cd backend
poetry run pytest tests/ -v
```

### 3. Execução em CI (GitHub Actions)
Os testes são executados automaticamente a cada `push` e `pull_request` no GitHub através do workflow definido em `.github/workflows/ci-backend.yml`.

## Como Executar a Aplicação

### Via Docker Compose (Ambiente Completo)
Na raiz do repositório:
```bash
make compose-up
```

### Desenvolvimento Local (Host)
```bash
make install
make run
```
