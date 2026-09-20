# DSN-DASH

Dashboard de análise **descritiva** de propagação de desinformação  
(WordPress + Elasticsearch/Kibana + Shiny) — **dados fictícios**, demo local.

## Subir a demo (5 passos)

1. Clone e entre na tag: `git clone … && git checkout v0.1.0`
2. Configure o ambiente: `cd docker && cp .env.example .env`
3. Suba os serviços: `docker compose up -d --build`
4. Bootstrap (seed + Kibana + plugin WP): `cd .. && py -3 scripts/demo_bootstrap.py`  
   (ou `python scripts/demo_bootstrap.py`)
5. Abra as páginas: [Por Tema](http://localhost:8080/por-tema/) · [Por Plataforma](http://localhost:8080/por-plataforma/)

## URLs e credenciais (dev)

| Serviço | URL |
|---------|-----|
| Painel Tema | http://localhost:8080/por-tema/ |
| Painel Plataforma | http://localhost:8080/por-plataforma/ |
| WP Admin | http://localhost:8080/wp-admin — `admin` / `adminchangeme` |
| Kibana | http://localhost:5601 |
| Shiny | http://localhost:3838/dsn/ |

## Documentação

| Fase | Pasta |
|------|--------|
| Discovery → Entrega | `docs/00-discovery` … `docs/07-delivery` |
| Manual de demo | [`docs/07-delivery/manual-demo.md`](docs/07-delivery/manual-demo.md) |
| Release notes | [`docs/07-delivery/release-notes.md`](docs/07-delivery/release-notes.md) |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) |

## Known issues (v0.1.0)

Ver [relatório QA](docs/06-validation/relatorio-qa.md): BUG-001 (scroll), BUG-002 (embeds Kibana), BUG-004 (ES na porta 9200).
