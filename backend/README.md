# Backend - C216 (Sistemas Distribuídos)

Este diretório contém o backend desenvolvido em Python com FastAPI, gerenciado via Poetry e conteinerizado com Docker.

## Dependências Principais
- **FastAPI**: Framework web moderno e de alta performance.
- **Uvicorn**: Servidor ASGI para execução da aplicação.
- **Pydantic**: Validação de dados e tipagem estrita.
- **Pytest & HTTPX**: Testes automatizados da API.

## Conteinerização
- **Dockerfile**: Imagem baseada em `python:3.11-slim`, com instalação do Poetry e cache inteligente de camadas.
- **.dockerignore**: Exclusão de arquivos temporários, caches e ambientes virtuais locais.

## Como Executar

### 1. Via Docker Compose (Ambiente Distribuído Completo)
Na raiz do projeto:
- `make compose-up`: Constrói as imagens e sobe os serviços do backend e banco de dados PostgreSQL.
- `make compose-logs`: Visualiza os logs dos containers em tempo real.
- `make compose-down`: Encerra e remove os containers.

### 2. Desenvolvimento Local (Direto no Host)
- `make install`: Instala as dependências via Poetry.
- `make run`: Inicia o servidor localmente com recarregamento automático (reload).
- `make test`: Executa a suíte de testes unitários com Pytest.
