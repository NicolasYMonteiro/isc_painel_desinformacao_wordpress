# ADR-002 — Docker Compose vs instalação local

| Campo | Valor |
|-------|-------|
| Status | **Accepted** |
| Data | 2026-09-20 |
| Origem | P-ENV discovery; US-009, US-017; RNF-003 |
| Destino | MOD-ES, MOD-KIBANA, MOD-SHINY, MOD-WP-PLUGIN, MOD-SEED |

## Contexto

A stack envolve WordPress, MySQL, Elasticsearch 8.x, Kibana e R/Shiny. Instalações manuais divergem entre máquinas e dificultam smoke test e onboarding.

## Decisão

Empacotar o ambiente de desenvolvimento/demo com **Docker Compose** (um arquivo de orquestração versionado em `docs/03-architecture/docker-compose.yml`, promovido à raiz na implementação).

## Consequências

- **Positivas:** reprodutibilidade; rede interna para esconder ES; parity de headers entre serviços; facilita MOD-SEED.
- **Negativas:** consumo de RAM/CPU (risco baixo RK-08); curva Docker para P3.
- **Escopo:** tags major provisórias (8.x / imagens oficiais); pin de patch em etapa posterior.

## Alternativas consideradas

| Alternativa | Motivo da rejeição |
|-------------|-------------------|
| Instalação local nativa de cada serviço | Drift de versões; framing/CORS difíceis de documentar |
| Apenas WP local + ES cloud | Fora do escopo demo self-contained; auth/ES público |

## Relacionados

[docker-compose.yml](../docker-compose.yml), [c4-container.md](../c4-container.md)
