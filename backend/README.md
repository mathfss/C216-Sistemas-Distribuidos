# Backend - C216 (Sistemas Distribuídos)

Este diretório contém o backend desenvolvido em Python com FastAPI, gerenciado via Poetry.

## Dependências Principais
- **FastAPI**: Framework web moderno e de alta performance.
- **Uvicorn**: Servidor ASGI rápido para rodar a aplicação.
- **Pydantic**: Validação de dados e schemas.
- **Pytest & HTTPX**: Testes automatizados da API.

## Como Executar

A partir da raiz do repositório, você pode utilizar os comandos definidos no `Makefile`:

- `make install`: Instala as dependências.
- `make run`: Inicia o servidor localmente com recarregamento automático (reload).
- `make test`: Executa a suíte de testes com Pytest.
