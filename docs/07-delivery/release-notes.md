# DSN-DASH — Release notes v0.1.0

| Campo | Valor |
|-------|-------|
| Versão | **0.1.0** |
| Tag | `v0.1.0` |
| Data | 2026-09-20 |
| Tipo | Demonstração local — dados fictícios |
| DELIVERABLE | DELIVERABLE-REL-001 |

## Escopo

Painel WordPress com duas páginas (**Por Tema** / **Por Plataforma**), carrossel lateral (4 slides cada), embeds Kibana + Shiny, seed Elasticsearch `desinfo_events` (~50k eventos sintéticos: 4 plataformas × 15 temas × 27 UFs × 2021–2024).

## Como subir

Ver [README.md](../../README.md) — **5 passos** + `scripts/demo_bootstrap.py`.

## URLs e credenciais (apenas demo)

| Recurso | Valor |
|---------|--------|
| Por Tema | http://localhost:8080/por-tema/ |
| Por Plataforma | http://localhost:8080/por-plataforma/ |
| WP Admin | `admin` / `adminchangeme` |
| MySQL | `wp` / `wpchangeme` (ver `docker/.env.example`) |

## Deliverables desta release

| ID | Descrição |
|----|-----------|
| DELIVERABLE-DEMO-001 | Stack Docker + plugin `dsn-dashboard` |
| DELIVERABLE-SEED-001 | Seed + índice `desinfo_events` |
| DELIVERABLE-QA-001 | Relatório QA + screenshots + matriz de testes |
| DELIVERABLE-DOCS-001 | Docs `00`–`07` |
| DELIVERABLE-REL-001 | Tag SemVer `v0.1.0` + estas notes |

## Known issues

Não bloqueiam a narrativa de demo (Shiny e shell WP funcionam); Kibana no iframe está degradado.

| ID | Severidade | Resumo |
|----|------------|--------|
| BUG-001 | Alta | Scroll vertical efetivo no host |
| BUG-002 | Alta | Embeds Kibana (CSP/404) |
| BUG-003 | Média | a11y listas do tema WP |
| BUG-004 | Alta | ES `:9200` exposto |
| BUG-005 | Média | Visual Kibana vs Shiny |

Fonte: [docs/06-validation/relatorio-qa.md](../06-validation/relatorio-qa.md).

## Fora de escopo

- Dados reais
- Auth de embeds em produção (RF-019 Won't)
- Deploy cloud / HTTPS produção
