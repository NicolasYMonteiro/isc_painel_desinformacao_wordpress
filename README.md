# DSN-DASH

Dashboard de análise **descritiva** de propagação de desinformação  
(WordPress + Elasticsearch/Kibana + Shiny) — **dados fictícios**, demo local.

## Subir a demo (5 passos)

1. Clone e entre na tag: `git clone … && git checkout v0.2.0`
2. Configure o ambiente: `cd docker && cp .env.example .env`
3. Suba os serviços: `docker compose up -d --build`
4. Bootstrap (seed + Kibana + plugin WP): `cd .. && py -3 scripts/demo_bootstrap.py`  
   (ou `python scripts/demo_bootstrap.py`)
5. Abra as páginas: [Por Tema](http://localhost:8080/por-tema/) · [Por Plataforma](http://localhost:8080/por-plataforma/)

> Elasticsearch **não** publica a porta `9200` no host (RNF-009). O bootstrap acessa o ES via rede Docker / `docker exec`.

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
| Validação mosaico | [`docs/06-validation/relatorio-mosaico.md`](docs/06-validation/relatorio-mosaico.md) |

## Release atual

**v0.2.0** — mosaico v2 + correções BUG-001…005. Ver [release notes](docs/07-delivery/release-notes.md).
