# DSN-DASH — Release notes

## [0.2.0] — 2026-09-21 — onda mosaico v2

| Campo | Valor |
|-------|-------|
| Versão | **0.2.0** |
| Tag | `v0.2.0` |
| Base | pós-`v0.1.0` |
| Tipo | Demonstração local — dados fictícios |

### Destaques

- Mosaicos **Padrões A–D** em Por Tema (T1–T4) e Por Plataforma (P1–P4)
- **RNF-003:** 1 dashboard Kibana multi-painel por slide (1 iframe)
- **RNF-005:** Vega alinhado aos tokens `--dsn-*` (fundo surface / accent sky)
- **BUG-001:** shell fullscreen sem scroll de página
- **BUG-004:** Elasticsearch sem publish `:9200` no host (seed via docker exec)
- **BUG-003:** chrome do tema WP com `aria-hidden` nas páginas do painel

### Known issues remanescentes

_Nenhum bug crítico aberto nesta release._ Ressalvas menores de chrome Kibana nativo podem persistir dentro do iframe.

### Como subir

Ver [README.md](../../README.md) — Compose + `scripts/demo_bootstrap.py`.

---

## [0.1.0] — 2026-09-20

| Campo | Valor |
|-------|-------|
| Versão | **0.1.0** |
| Tag | `v0.1.0` |
| Tipo | Demonstração local — dados fictícios |
| DELIVERABLE | DELIVERABLE-REL-001 |

### Escopo

Painel WordPress com duas páginas (**Por Tema** / **Por Plataforma**), carrossel lateral (4 slides cada), embeds Kibana + Shiny, seed Elasticsearch `desinfo_events` (~50k eventos sintéticos: 4 plataformas × 15 temas × 27 UFs × 2021–2024).

### Known issues (histórico v0.1.0)

| ID | Severidade | Resumo | Status em 0.2.0 |
|----|------------|--------|-----------------|
| BUG-001 | Alta | Scroll vertical efetivo no host | **Corrigido** |
| BUG-002 | Alta | Embeds Kibana CSP/TypeError | **Corrigido** |
| BUG-003 | Média | a11y listas do tema WP | **Corrigido** |
| BUG-004 | Alta | ES `:9200` exposto | **Corrigido** |
| BUG-005 | Média | Área de gráfico Kibana vazia | **Corrigido** |

### Fora de escopo

- Dados reais
- Auth de embeds em produção (RF-019 Won't)
- Deploy cloud / HTTPS produção
