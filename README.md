# URL Shortener API

API para encurtamento de URLs construída com FastAPI, incluindo cache com Redis e proteção contra DDoS.

## Funcionalidades

- Encurtamento de URLs
- Cache com Redis
- Rate limiting por IP
- Documentação Swagger
- Proteção contra DDoS

## Requisitos

- Python 3.8+
- Docker e Docker Compose
- Redis (via Docker)

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o Redis usando Docker Compose:
```bash
docker-compose up -d
```

5. Configure as variáveis de ambiente no arquivo `.env`

## Executando a API

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação

A documentação Swagger está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST /shorten
Encurta uma URL.

Exemplo de requisição:
```json
{
    "url": "https://www.exemplo.com"
}
```

### GET /{short_code}
Redireciona para a URL original usando o código curto.

## Rate Limiting

- Limite padrão: 100 requisições por hora por IP
- Configurável através das variáveis de ambiente:
  - RATE_LIMIT_REQUESTS
  - RATE_LIMIT_PERIOD 