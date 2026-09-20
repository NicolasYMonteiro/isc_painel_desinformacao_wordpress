# ADR-004 — Estratégia de homogeneização visual

| Campo | Valor |
|-------|-------|
| Status | **Accepted** |
| Data | 2026-09-20 |
| Origem | RNF-005, RNF-008; US-008; RF-008 |
| Destino | MOD-WP-PLUGIN, MOD-CAROUSEL, MOD-KIBANA, MOD-SHINY |

## Contexto

Gráficos Kibana e Shiny devem parecer do mesmo produto (paleta ≥4 tokens, tipografia do shell, padding externo ±8 px). Iframes são **cross-origin** em relação ao WP.

## Decisão

Homogeneizar via:

1. **Wrapper CSS no host** (`.dsn-embed-frame`, tokens `--dsn-*`) — borda, fundo, tipografia da legenda, padding externo medido.
2. **Theming dos filhos na origem:** parâmetros/URL de embed Kibana (esconder chrome quando suportado) + tema/CSS do app Shiny alinhado aos tokens.
3. **Não** injetar CSS dentro do documento do iframe cross-origin (bloqueado pela same-origin policy).

## Consequências

- **Positivas:** viável tecnicamente; mensurável (checklist RNF-005); shell WCAG no host (RNF-008).
- **Negativas:** chrome residual do Kibana pode vazar; exige disciplina de tema Shiny.
- **Same-origin futuro:** reverse proxy poderia unificar origem e facilitar theming — fora do MVP; não muda esta ADR.

## Alternativas consideradas

| Alternativa | Motivo da rejeição |
|-------------|-------------------|
| CSS injection no iframe | Inviável cross-origin sem cooperação do filho |
| Só screenshots estáticos | Perde interatividade Kibana/Shiny; foge do escopo embeds |

## Relacionados

[design-carrossel.md](../design-carrossel.md), [ADR-001](./ADR-001-iframe-vs-api.md)
