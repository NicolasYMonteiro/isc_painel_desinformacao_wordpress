# DSN-DASH — Biblioteca de padrões de mosaico (A–D)


| Campo       | Valor                                                              |
| ----------- | ------------------------------------------------------------------ |
| Fase        | Refinamento pós-implementação (design)                             |
| Origem      | RF-001..003, RNF-001, RNF-003, RNF-005                             |
| Destino     | TASK-008b, TASK-009b, TASK-010b                                    |
| Sucessor de | [design-carrossel.md](./design-carrossel.md) (v1: 1 gráfico/slide) |
| Wireframes  | [design-carrossel-v2.md](./design-carrossel-v2.md)                 |
| Data        | 2026-09-20                                                         |
| Status      | **Implementado** (TASK-008b / 009b / 010b + RNF-003 multi-painel) |


---

## Objetivo

Substituir o modelo “1 gráfico por slide” por um **mosaico coerente** de componentes analíticos (KPIs + barras + série temporal), com densidade próxima a painéis de referência (ex.: PCDaS/Fiocruz), sem alterar o mecanismo Swiper nem introduzir scroll vertical na página-host.

---

## Regras transversais (todos os padrões)

1. **Uma pergunta analítica por slide** — todos os componentes respondem à mesma pergunta.
2. **Uma fatia de dados** — filtro único: `theme=…` | `platform=…` | visão global | lente geográfica. Sem misturar fatias no mesmo slide.
3. **Mínimo obrigatório:** ≥ 3 KPIs numéricos + ≥ 1 gráfico de barras estratificado + ≥ 1 série temporal (linha, 2021–2024, granularidade **mensal**).
4. **KPI:** valor, rótulo, variação % YoY (**2024 vs 2023**), seta ↑/↓ + cor, período de referência explícito.
5. **Grid:** CSS Grid **12 colunas**; gaps alinhados a `--dsn-embed-pad`.
6. **Viewport:** mosaico cabe em `100vh − header` em desktop ≥ 1280px (sem scroll de página). Mobile: 1 coluna; scroll **somente dentro do `.dsn-slide`**.
7. **Homogeneidade (RNF-005 / ADR-004):** paleta/tipografia/espaçamento via tokens `--dsn-`*; Kibana e Shiny espelham no filho.
8. **Carrossel:** Swiper permanece (`slidesPerView: 1`, < 300 ms, teclado, indicador n/4).

### Tokens reutilizados


| Token                 | Uso no mosaico                   |
| --------------------- | -------------------------------- |
| `--dsn-color-bg`      | Fundo do shell / slide           |
| `--dsn-color-surface` | Cards KPI e painéis de gráfico   |
| `--dsn-color-accent`  | Destaque Δ% positivo / controles |
| `--dsn-color-text`    | Rótulos e valores                |
| `--dsn-font-family`   | Tipografia do shell e KPIs       |
| `--dsn-embed-pad`     | Gap do grid e padding interno    |


Sugestão de tokens adicionais (implementação TASK-008b): `--dsn-kpi-up` / `--dsn-kpi-down` para Δ%.

### Checklist por slide

- [x] Pergunta analítica declarada
- [ ] Fatia de dados única documentada
- [ ] ≥ 3 KPIs com Δ% 2024 vs 2023
- [ ] ≥ 1 barra estratificada
- [ ] ≥ 1 linha temporal mensal (4 anos)
- [ ] Layout 12-col documentado
- [ ] Cabe em 100vh desktop; mobile = scroll-in-slide

---

## Catálogo de padrões


| ID    | Nome                | Layout resumido                                             | Obrigatórios                           | Opcional         |
| ----- | ------------------- | ----------------------------------------------------------- | -------------------------------------- | ---------------- |
| **A** | Corte temático      | KPIs 3–4 → linha full → barras 6+6                          | KPI, linha, barras plataforma + top UF | —                |
| **B** | Corte de plataforma | KPIs → linha 8 + heatmap 4 → barras temas full              | KPI, linha, barras temas               | heatmap Tema×Ano |
| **C** | Visão cruzada       | KPIs → barras empilhadas full → linha 6 + donut 6           | KPI, barras Tema×Plat, linha           | donut share      |
| **D** | Geografia           | KPIs → mapa/barras região 6 + top UF 6 → linha macrorregião | KPI, ranking UF, linha N/NE/CO/SE/S    | choropleth UF    |


---

## Padrão A — Corte temático

**Fatia:** `theme=<slug>` (ex.: `eleicao`, `vacinas`).  
**Uso:** slides T2, T3.

```
┌──────────────────────────────────────────────┐
│  Título: {TEMA} · 2021–2024                  │
├─────────┬─────────┬─────────┬────────────────┤
│ KPI 1   │ KPI 2   │ KPI 3   │  KPI 4 (opc.)  │  ← span 3+3+3+3
├─────────┴─────────┴─────────┴────────────────┤
│                                              │
│   LINHA TEMPORAL (mensal, 4 anos)            │  ← span 12
│                                              │
├──────────────────────┬───────────────────────┤
│ BARRAS por PLATAFORMA│ BARRAS Top 10 UF      │  ← span 6+6
└──────────────────────┴───────────────────────┘
```


| Slot     | Tipo         | Spec                                                                            |
| -------- | ------------ | ------------------------------------------------------------------------------- |
| KPI 1–4  | host         | Eventos 2024; Engajamento Σ 2024; Δ% eventos YoY; Share do tema no total (opc.) |
| Linha    | Kibana/Shiny | Contagem mensal no tema                                                         |
| Barras L | Kibana/Shiny | Eventos por plataforma (filtrado ao tema)                                       |
| Barras R | Kibana/Shiny | Top 10 UF no tema                                                               |


---

## Padrão B — Corte de plataforma

**Fatia:** `platform=<slug>` (ex.: `whatsapp`, `youtube`, `facebook`).  
**Uso:** slides P2, P3, P4.

```
┌──────────────────────────────────────────────┐
│  Título: {PLATAFORMA} · 2021–2024            │
├─────────┬─────────┬─────────┬────────────────┤
│ KPI 1   │ KPI 2   │ KPI 3   │  KPI 4 (opc.)  │
├─────────────────────────────┬────────────────┤
│                             │                │
│  LINHA TEMPORAL (mensal)    │ HEATMAP        │  ← span 8+4
│                             │ Tema × Ano     │
├─────────────────────────────┴────────────────┤
│  BARRAS: Top 10 temas nesta plataforma       │  ← span 12
└──────────────────────────────────────────────┘
```


| Slot    | Tipo  | Spec                                                              |
| ------- | ----- | ----------------------------------------------------------------- |
| KPI 1–4 | host  | Eventos 2024; Engajamento Σ; Δ% YoY; Share da plataforma no total |
| Linha   | embed | Contagem mensal na plataforma                                     |
| Heatmap | embed | Tema × Ano (contagens)                                            |
| Barras  | embed | Top 10 temas na plataforma                                        |


---

## Padrão C — Visão cruzada

**Fatia:** global (sem filtro theme/platform), ângulo tema **ou** plataforma conforme a página.  
**Uso:** slides T1, P1.

```
┌──────────────────────────────────────────────┐
│  Título: PLATAFORMAS × TEMAS (2021–2024)     │
├─────────┬─────────┬─────────┬────────────────┤
│ KPI 1   │ KPI 2   │ KPI 3   │  KPI 4         │
├──────────────────────────────────────────────┤
│  BARRAS EMPILHADAS: Tema × Plataforma        │  ← span 12
├──────────────────────┬───────────────────────┤
│ LINHA: Evolução total│ DONUT: Share por plat.│  ← span 6+6
└──────────────────────┴───────────────────────┘
```


| Slot              | Tipo  | Spec                                                                            |
| ----------------- | ----- | ------------------------------------------------------------------------------- |
| KPI 1–4           | host  | Total eventos 2024; Engajamento Σ; Δ% YoY global; Nº temas ativos / plataformas |
| Barras empilhadas | embed | Volume por tema empilhado por plataforma (ou inverso no ângulo P1)              |
| Linha             | embed | Total mensal global                                                             |
| Donut             | embed | Share por plataforma (P1 enfatiza; T1 idem)                                     |


---

## Padrão D — Geografia

**Fatia:** lente UF / macrorregião (sem filtro theme/platform único).  
**Uso:** slide T4.

```
┌──────────────────────────────────────────────┐
│  Título: DISTRIBUIÇÃO GEOGRÁFICA             │
├─────────┬─────────┬─────────┬────────────────┤
│ KPI 1   │ KPI 2   │ KPI 3   │  KPI 4         │
├──────────────────────┬───────────────────────┤
│  MAPA/CHOROPLETH UF  │  BARRAS: Top 10 UFs   │  ← span 6+6
│  (ou barras região)  │                       │
├──────────────────────┴───────────────────────┤
│  LINHA TEMPORAL por região (N/NE/CO/SE/S)    │  ← span 12
└──────────────────────────────────────────────┘
```


| Slot    | Tipo  | Spec                                                                                          |
| ------- | ----- | --------------------------------------------------------------------------------------------- |
| KPI 1–4 | host  | Eventos 2024; UF líder; Δ% YoY da UF líder; Concentração top-5 UF (%)                         |
| Mapa    | embed | Choropleth UF **se viável**; senão barras por macrorregião (fallback obrigatório documentado) |
| Barras  | embed | Top 10 UF                                                                                     |
| Linha   | embed | Série mensal por macrorregião (5 séries)                                                      |


---

## Nota técnica de implementação (pós-aprovação)

**Preferência:** KPIs renderizados no **host** (PHP/JS a partir de agregações pré-calculadas ou API interna) + **1 dashboard Kibana multi-painel** (ou 1 app Shiny multi-plot) por slide — evitar N iframes (risco RNF-003: 1º embed útil < 5 s).

Não implementar nesta fase de design.

---

## Aprovação


| Item                     | Status                                                 |
| ------------------------ | ------------------------------------------------------ |
| Padrões A/B/C/D          | Pendente feedback do stakeholder                       |
| Mapeamento T1–T4 / P1–P4 | Ver [design-carrossel-v2.md](./design-carrossel-v2.md) |


Próximo passo após aprovação: executar **TASK-008b** (shell CSS Grid).