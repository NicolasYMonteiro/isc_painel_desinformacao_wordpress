# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).  
Versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [0.2.0] - 2026-09-21

### Added

- Mosaico v2 completo: T1–T4 (C/A/A/D) e P1–P4 (C/B/B/B) com KPIs nativos Δ% 2024 vs 2023
- Dashboards Kibana **multi-painel** (1 iframe/slide) — RNF-003
- Suite E2E `mosaic-validacao-v2` + relatório `docs/06-validation/relatorio-mosaico.md`
- Cliente ES via `docker exec` quando a porta host não está publicada (`scripts/seed/es_http.py`)

### Fixed

- **BUG-001** — shell fullscreen / chrome WP oculto / sem scroll de página
- **BUG-002 / BUG-005** — embeds Kibana Vega + janela 2021–2024
- **BUG-003** — `aria-hidden`/`inert` no chrome do tema nas páginas do painel
- **BUG-004** — Elasticsearch sem `ports:` no Compose (RNF-009)
- **RNF-005** — paleta Vega alinhada a `--dsn-color-surface` / `--dsn-color-accent`

## [0.1.0] - 2026-09-20

### Added

- Stack Docker Compose (`wordpress`, `mysql`, `elasticsearch`, `kibana`, `shiny`) na rede `dsn-net`
- Plugin WordPress `dsn-dashboard` com shortcode, carrossel Swiper (4 slides × 2 páginas), badge de dados fictícios
- Seed reprodutível (~50 000 docs) no índice `desinfo_events` + dataset Shiny
- Script `scripts/demo_bootstrap.py` (seed + Kibana + ativação do plugin)
- Documentação MEGA: discovery → requisitos → US → arquitetura → tasks → validação → entrega
- Suite E2E Playwright + axe (`tests/e2e/`)

### Known issues (na tag 0.1.0; corrigidos em 0.2.0)

- **BUG-001** — scroll vertical efetivo no host
- **BUG-003** — axe serious em listas do tema WP
- **BUG-004** — Elasticsearch publicado em `:9200`

### Out of scope

- Autenticação de embeds em produção (RF-019 / TASK-019 Won't)
- Dados reais / PII

[0.2.0]: https://github.com/NicolasYMonteiro/isc_painel_desinformacao_wordpress/releases/tag/v0.2.0
[0.1.0]: https://github.com/NicolasYMonteiro/isc_painel_desinformacao_wordpress/releases/tag/v0.1.0
