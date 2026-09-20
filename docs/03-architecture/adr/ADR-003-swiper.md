# ADR-003 — Swiper.js vs carrossel custom

| Campo | Valor |
|-------|-------|
| Status | **Accepted** |
| Data | 2026-09-20 |
| Origem | RNF-001, RNF-002, RNF-006; US-003, US-014 |
| Destino | MOD-CAROUSEL, MOD-WP-PLUGIN |

## Contexto

O produto exige carrossel lateral sem scroll no host, 4 slides por página, transição &lt; 300 ms, controles + indicador e operação por teclado com foco visível.

## Decisão

Usar **Swiper.js** como biblioteca do carrossel no plugin `dsn-dashboard` (assets enfileirados pelo WordPress), configurado para: uma slide por view, navegação horizontal, teclado habilitado, paginação/indicador, velocidade de transição compatível com RNF-001.

## Consequências

- **Positivas:** a11y e teclado maduros; menos código custom; atende RNF-001/006 com configuração.
- **Negativas:** dependência front externa (versão a pinar na implementação); CSS do Swiper deve ser sobrescrito pelos tokens DSN.
- **Integração:** estados `loading|ready|error|empty` no DOM do slide (fora do core Swiper) — ver design-carrossel.

## Alternativas consideradas

| Alternativa | Motivo da rejeição |
|-------------|-------------------|
| Carrossel 100% JS puro custom | Custo de a11y/teclado/foco; risco a RNF-006 |
| Só CSS scroll-snap | Difícil garantir “sem scroll” no host + indicador acessível |

## Relacionados

[design-carrossel.md](../design-carrossel.md), [ADR-004](./ADR-004-homogeneizacao-visual.md)
