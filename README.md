# DSN-DASH

Dashboard de análise descritiva de propagação de desinformação (WordPress + Elasticsearch/Kibana + Shiny).

## Docs

- Discovery: `docs/00-discovery/`
- Requisitos: `docs/01-requirements/`
- User stories: `docs/02-user-stories/`
- Arquitetura: `docs/03-architecture/`
- Tasks: `docs/04-tasks/`

## Quick start

```bash
cd docker
cp .env.example .env
docker compose up -d --build
```

Seed (~50k docs):

```bash
pip install -r requirements.txt
python scripts/seed/generate_data.py
python scripts/seed/index_to_es.py --recreate
python scripts/seed/validate_catalogs.py
```

Testes:

```bash
pytest -q
```

## TASK-019 (Won't)

Autenticação de embeds em produção **fora deste incremento**. Demo local sem auth.

## URLs locais

| Serviço | URL |
|---------|-----|
| WP | http://localhost:8080 |
| ES | http://localhost:9200 |
| Kibana | http://localhost:5601 |
| Shiny | http://localhost:3838/dsn/ |
