# URL Shortener API

API para encurtamento de URLs construída com FastAPI, incluindo cache em memória com persistência e proteção contra DDoS.

## Funcionalidades

- Encurtamento de URLs
- Redirecionamento automático
- Estatísticas de acesso
- Cache em memória com persistência em JSON
- Proteção contra DDoS
- Rate limiting
- Validação de URLs
- Logging centralizado

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/url-shortener-python-ai.git
cd url-shortener-python-ai
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicie a aplicação:
```bash
uvicorn app.main:app --reload
```

## Uso

A API estará disponível em `http://localhost:8000`. Você pode acessar a documentação automática em `http://localhost:8000/docs`.

### Endpoints Principais

- `POST /api/v1/shorten` - Criar uma nova URL encurtada
- `GET /{short_code}` - Redirecionar para a URL original
- `GET /api/v1/stats/{short_code}` - Obter estatísticas da URL
- `GET /api/v1/urls` - Listar todas as URLs
- `DELETE /api/v1/{short_code}` - Excluir uma URL
- `PUT /api/v1/{short_code}` - Atualizar uma URL
- `GET /api/v1/health` - Verificar o status da API

### Exemplo de Uso

1. Encurtar uma URL:
```bash
curl -X POST "http://localhost:8000/api/v1/shorten" -H "Content-Type: application/json" -d '{"url": "https://www.exemplo.com"}'
```

2. Acessar a URL encurtada:
```
http://localhost:8000/abc123
```

## Segurança

- Rate limiting por IP
- Validação de URLs
- Proteção contra DDoS
- Logging de atividades suspeitas
- Sanitização de entrada

## Logging

Os logs são armazenados no diretório `logs/` com rotação automática:
- `api.log` - Logs gerais da API
- `security.log` - Logs de segurança
- `memory.log` - Logs do repositório em memória

## Persistência de Dados

As URLs encurtadas e suas estatísticas são armazenadas em um arquivo JSON no diretório `data/`. Isso garante que os dados não sejam perdidos quando a aplicação for reiniciada.

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 