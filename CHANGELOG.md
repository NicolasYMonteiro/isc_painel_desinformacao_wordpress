# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).  
Versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2026-09-20

### Added

- Stack Docker Compose (`wordpress`, `mysql`, `elasticsearch`, `kibana`, `shiny`) na rede `dsn-net`
- Plugin WordPress `dsn-dashboard` com shortcode, carrossel Swiper (4 slides × 2 páginas), badge de dados fictícios
- Seed reprodutível (~50 000 docs) no índice `desinfo_events` + dataset Shiny
- Script `scripts/demo_bootstrap.py` (seed + Kibana + ativação do plugin)
- Documentação MEGA: discovery → requisitos → US → arquitetura → tasks → validação → entrega
- Suite E2E Playwright + axe (`tests/e2e/`)

### Known issues

- **BUG-001** — scroll vertical efetivo no host (tema WP + viewport)
- **BUG-002** — embeds Kibana com CSP/404/TypeError no iframe
- **BUG-003** — axe serious em listas do tema WP
- **BUG-004** — Elasticsearch publicado em `:9200` (acessível ao browser na demo)
- **BUG-005** — slides Kibana visualmente degradados vs Shiny

Detalhes: [`docs/06-validation/relatorio-qa.md`](docs/06-validation/relatorio-qa.md).

### Out of scope

- Autenticação de embeds em produção (RF-019 / TASK-019 Won't)
- Dados reais / PII

[0.1.0]: https://github.com/NicolasYMonteiro/isc_painel_desinformacao_wordpress/releases/tag/v0.1.0
