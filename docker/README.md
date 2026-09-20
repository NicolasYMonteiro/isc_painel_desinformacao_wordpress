# Docker — DSN-DASH (TASK-001)

## Subir o ambiente

```bash
cd docker
cp .env.example .env
docker compose up -d --build
```

Aguarde os healthchecks (`docker compose ps`).

## URLs

| Serviço | URL |
|---------|-----|
| WordPress | http://localhost:8080 |
| Elasticsearch | http://localhost:9200 |
| Kibana | http://localhost:5601 |
| Shiny (app DSN) | http://localhost:3838/dsn/ |

## Credenciais default (dev)

| Item | Valor |
|------|-------|
| MySQL database | `wordpress` |
| MySQL user | `wp` / `wpchangeme` |
| MySQL root | `rootchangeme` |
| WP | configurar no primeiro acesso (instalação WP) |
| ES / Kibana | sem auth (`xpack.security.enabled=false`) |

**Nunca** use estas senhas em produção. Credenciais ficam em `.env` (não commitado).

## Plugin

Volume monta `wp-content/plugins/dsn-dashboard`. Ative o plugin no admin WP após a instalação.

## Seed (próximo: TASK-002/003)

```bash
# na raiz do repo
python -m pip install -r requirements.txt
python scripts/seed/generate_data.py
python scripts/seed/index_to_es.py --es http://localhost:9200 --recreate
```

## Smoke

```bash
docker compose -f docker/docker-compose.yml config
curl -fsS http://localhost:9200
curl -fsS http://localhost:5601/api/status
curl -fsS http://localhost:8080
curl -fsS http://localhost:3838/dsn/
```

## Rede e volumes

- Rede: `dsn-net`
- Volumes: `dsn-wp-data`, `dsn-mysql-data`, `dsn-es-data`
