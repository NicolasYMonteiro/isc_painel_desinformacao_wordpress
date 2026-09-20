# Retrospectiva — incremento DSN-DASH v0.1.0

| Campo | Valor |
|-------|-------|
| Período | Discovery → Entrega (2026-09-20) |
| Release | v0.1.0 |
| DELIVERABLE | DELIVERABLE-DOCS-001 / REL-001 |

## O que funcionou bem

- Pipeline MEGA documentado (discovery → REQ → US → ADR → TASK → QA → entrega) com rastreabilidade
- Docker Compose unificou WP + ES + Kibana + Shiny o suficiente para demo local
- Seed dimensional reprodutível (50k) e validação de catálogos
- Plugin shortcode + Swiper atenderam carrossel, teclado e tempos de transição (&lt;300 ms)
- Shiny com theming alinhado aos tokens DSN entregou slides úteis na demo
- Suite Playwright/axe gerou evidências objetivas (métricas + screenshots)

## O que não funcionou bem

- Embeds Kibana no iframe (CSP/404) — valor Kibana subutilizado na UI
- Scroll do host (tema WP) vs requisito “sem scroll” — conflito shell vs tema
- ES publicado em `:9200` por conveniência de seed, em tensão com RNF-009
- Build Shiny inicial com `install.packages` alongou o primeiro `compose up`
- Auth `gh` e branch `main` vazia atrasaram o primeiro PR

## Lições aprendidas

1. **Provar embed Kibana cedo** (spike TASK-004) antes de depender dele no carrossel
2. **Tema WP minimalista** dedicado ao painel evita lutar com chrome do tema default
3. **ES só na rede Docker** + seed via `docker exec` / network interna evita violar RNF-009
4. **Bootstrap único** (`demo_bootstrap.py`) é obrigatório para demo em ≤5 passos
5. Separar “demo narrativa” (Shiny estável) de “fonte Kibana” reduz risco comercial

## Backlog futuro (não nesta tag)

| Item | Motivação |
|------|-----------|
| Dados reais (pipeline ETL + LGPD) | Substituir seed fictício |
| Corrigir BUG-002 (Kibana embed) | Completar RF-006 |
| Corrigir BUG-001 (scroll/host) | Cumprir RNF-002 |
| Não publicar ES no host (BUG-004) | Cumprir RNF-009 |
| Mais fontes / plataformas | Expandir domínio além das 4 |
| Auth embeds / ambientes (RF-019) | Produção |
| Homogeneidade visual ponta a ponta | Chrome Kibana vs tokens |
| CI E2E no GitHub Actions | Gate de regressão |

## Ação imediata pós-release

Priorizar BUG-001 e BUG-002 em sprint de estabilização; manter v0.1.0 como baseline de demo com known issues explícitos.
