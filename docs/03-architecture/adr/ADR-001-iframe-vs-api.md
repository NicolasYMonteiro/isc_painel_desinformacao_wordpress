# ADR-001 — Iframe vs API para visualizações

| Campo | Valor |
|-------|-------|
| Status | **Accepted** |
| Data | 2026-09-20 |
| Origem | RNF-004, RNF-009, RNF-011; US-006, US-007, US-020 |
| Destino | MOD-KIBANA, MOD-SHINY, MOD-WP-PLUGIN; API-ES (interna apenas) |

## Contexto

O painel precisa exibir gráficos de Elasticsearch/Kibana e de R/Shiny dentro do WordPress, com isolamento de segurança (ES inacessível ao browser) e framing configurável.

## Decisão

Usar **iframe** para embutir Kibana e Shiny no shell WordPress. O browser **não** consome API do Elasticsearch diretamente.

## Consequências

- **Positivas:** isolamento de origem; reutiliza UIs prontas; alinha RNF-009; CORS irrelevante para display.
- **Negativas:** depende de `frame-ancestors` / ausência de XFO bloqueante; cookies cross-site em prod; homogeneidade visual limitada (ADR-004).
- **Operação:** Kibana `disableEmbedding: false` + `csp.frame_ancestors` com origem WP; Shiny com CSP equivalente.

## Alternativas consideradas

| Alternativa | Motivo da rejeição |
|-------------|-------------------|
| Browser → API ES + charts no WP | Expõe ES (viola RNF-009); reimplementa UI Kibana |
| Server-side proxy HTML | Complexidade alta; ainda precisa framing/CSP cuidadoso |

## Relacionados

[ADR-004](./ADR-004-homogeneizacao-visual.md), [c4-container.md](../c4-container.md), [docker-compose.yml](../docker-compose.yml)
