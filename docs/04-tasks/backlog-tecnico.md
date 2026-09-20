# DSN-DASH — Backlog técnico

| Campo | Valor |
|-------|-------|
| Projeto | DSN-DASH |
| Fase MEGA | Planejamento |
| Origem | [US backlog](../02-user-stories/backlog.md), [MOD-*](../03-architecture/c4-container.md), ADRs |
| Destino | PR-*, TEST-* |
| Data | 2026-09-20 |

**DoD padrão** (exceto TASK-019): (1) código/config no módulo, (2) teste TEST-*, (3) doc atualizada, (4) pronto para PR-*.

---

## Ondas de execução (risco → valor)

| Onda | TASK | Foco |
|------|------|------|
| 0 — Infra | 001 | Compose + rede safe |
| 1 — Dados | 002, 003, 018 | Índice + seed + catálogos |
| 2 — Visualizações backend | 004, 005 | Kibana + Shiny (framing) |
| 3 — Shell WP | 006, 007, 008, 015 | Plugin, páginas, carrossel, badge |
| 4 — Conteúdo slides | 009, 010, 014 | 4+4 slides, legendas, descritivo |
| 5 — Embeds + UX | 011, 012, 013, 016, 017 | iframes, homogeneidade, estados |
| 6 — Fechamento | 020 | Smoke E2E |
| — Adiada | 019 | Auth produção (Won't) |

---

## Catálogo TASK-001..020

### TASK-001 — Promover Compose + rede safe (ES interno)

- **US:** US-009 (pré-requisito operacional)
- **MOD:** MOD-ES, MOD-WP-PLUGIN, MOD-KIBANA, MOD-SHINY
- **Depends-on:** nenhuma
- **Risco:** Alto (bloqueia tudo)
- **Destino:** PR-001, TEST-001
- **DoD:**
  - Código: `docker-compose.yml` na raiz (a partir do rascunho em `docs/03-architecture/`), rede bridge, ES sem publish público
  - Teste: `docker compose config` válido; serviços sobem (smoke parcial)
  - Doc: nota de portas/origens em README ou `docs/03-architecture`

### TASK-002 — Criar índice `desinfo_events` (mapping)

- **US:** US-009, US-010, US-011
- **MOD:** MOD-ES
- **Depends-on:** TASK-001
- **Risco:** Alto
- **Destino:** PR-002, TEST-002
- **DoD:**
  - Código: script/mapping alinhado a [schema-elasticsearch.md](../03-architecture/schema-elasticsearch.md)
  - Teste: índice criado; mapping confere campos obrigatórios
  - Doc: comando de create-index documentado

### TASK-003 — Gerador + carga seed ES + dataset Shiny

- **US:** US-009, US-017
- **MOD:** MOD-SEED
- **Depends-on:** TASK-002
- **Risco:** Alto
- **Destino:** PR-003, TEST-003
- **DoD:**
  - Código: gerador reprodutível + bulk ES + arquivos para volume Shiny
  - Teste: cobertura dimensional (4 plataformas × 15 temas × 27 UFs × 2021–2024); 0 PII real
  - Doc: procedimento de reaplicar seed (US-017)

### TASK-004 — Kibana: framing + dashboards embed

- **US:** US-006
- **MOD:** MOD-KIBANA
- **Depends-on:** TASK-003
- **Risco:** Alto (framing)
- **Destino:** PR-004, TEST-004
- **DoD:**
  - Código: `kibana.yml` com `disableEmbedding: false` + `frame_ancestors` WP; ≥1 dashboard embeddable
  - Teste: iframe em página de teste sem erro de framing (RNF-004)
  - Doc: URLs de embed documentadas

### TASK-005 — Shiny: app + framing + tema tokens

- **US:** US-007
- **MOD:** MOD-SHINY
- **Depends-on:** TASK-003
- **Risco:** Alto (framing/tema)
- **Destino:** PR-005, TEST-005
- **DoD:**
  - Código: app Shiny com gráficos descritivos; headers/`frame-ancestors`; tokens alinhados ADR-004
  - Teste: iframe sem framing error; lê seed montado
  - Doc: URL do app + dependências R

### TASK-006 — Scaffold plugin `dsn-dashboard` + shortcode

- **US:** US-001, US-002
- **MOD:** MOD-WP-PLUGIN
- **Depends-on:** TASK-001
- **Risco:** Médio
- **Destino:** PR-006, TEST-006
- **DoD:**
  - Código: plugin ativável; shortcode `[dsn_dashboard page="tema"|"plataforma"]` conforme contrato C4
  - Teste: shortcode renderiza shell HTML com classes `.dsn-dashboard`
  - Doc: README do plugin

### TASK-007 — Páginas WP Tema/Plataforma + nav (2 rotas)

- **US:** US-001, US-002, US-013
- **MOD:** MOD-WP-PLUGIN
- **Depends-on:** TASK-006
- **Risco:** Médio
- **Destino:** PR-007, TEST-007
- **DoD:**
  - Código: exatamente 2 páginas principais + navegação entre elas
  - Teste: RNF-012 (contagem = 2); alternância sem URL manual
  - Doc: slugs/URLs das páginas

### TASK-008 — Carrossel Swiper (sem scroll, teclado, indicador)

- **US:** US-003, US-014
- **MOD:** MOD-CAROUSEL
- **Depends-on:** TASK-006
- **Risco:** Médio
- **Destino:** PR-008, TEST-008
- **DoD:**
  - Código: Swiper (ADR-003); overflow host hidden; prev/next + indicador; teclado
  - Teste: RNF-001 (&lt;300 ms), RNF-002, RNF-006
  - Doc: referência a [design-carrossel.md](../03-architecture/design-carrossel.md)

### TASK-009 — Conteúdo 4 slides página Tema

- **US:** US-004, US-015
- **MOD:** MOD-CAROUSEL, MOD-WP-PLUGIN
- **Depends-on:** TASK-007, TASK-008
- **Risco:** Médio
- **Destino:** PR-009, TEST-009
- **DoD:**
  - Código: 4 slides em `page=tema`; eixo tema dominante
  - Teste: exatamente 4 slides com slot de gráfico
  - Doc: mapa slide → tipo embed

### TASK-010 — Conteúdo 4 slides página Plataforma

- **US:** US-005, US-015
- **MOD:** MOD-CAROUSEL, MOD-WP-PLUGIN
- **Depends-on:** TASK-007, TASK-008
- **Risco:** Médio
- **Destino:** PR-010, TEST-010
- **DoD:**
  - Código: 4 slides em `page=plataforma`; eixo plataforma dominante
  - Teste: exatamente 4 slides com slot de gráfico
  - Doc: mapa slide → tipo embed

### TASK-011 — Wire iframes Kibana nos slides

- **US:** US-006
- **MOD:** MOD-WP-PLUGIN, MOD-KIBANA
- **Depends-on:** TASK-004, TASK-009, TASK-010
- **Risco:** Alto
- **Destino:** PR-011, TEST-011
- **DoD:**
  - Código: ≥1 iframe Kibana por página; `title` não vazio; `data-embed-type=kibana`
  - Teste: 0 erros framing; RNF-007
  - Doc: env vars `DSN_KIBANA_URL`

### TASK-012 — Wire iframes Shiny nos slides

- **US:** US-007
- **MOD:** MOD-WP-PLUGIN, MOD-SHINY
- **Depends-on:** TASK-005, TASK-009, TASK-010
- **Risco:** Alto
- **Destino:** PR-012, TEST-012
- **DoD:**
  - Código: ≥1 iframe Shiny por página; `title`; `data-embed-type=shiny`
  - Teste: 0 erros framing
  - Doc: env vars `DSN_SHINY_URL`

### TASK-013 — Homogeneização visual (wrapper + tokens)

- **US:** US-008
- **MOD:** MOD-WP-PLUGIN, MOD-CAROUSEL
- **Depends-on:** TASK-011, TASK-012
- **Risco:** Médio
- **Destino:** PR-013, TEST-013
- **DoD:**
  - Código: `.dsn-embed-frame` + tokens `--dsn-*` (ADR-004); tema Shiny alinhado
  - Teste: checklist RNF-005 (paleta ≥4, tipografia, padding ±8 px)
  - Doc: lista de tokens

### TASK-014 — Legendas + revisão analítica descritiva

- **US:** US-012, US-016
- **MOD:** MOD-WP-PLUGIN
- **Depends-on:** TASK-009, TASK-010
- **Risco:** Baixo
- **Destino:** PR-014, TEST-014
- **DoD:**
  - Código: legenda curta nos 8 slides; sem ML/estatística complexa
  - Teste: revisão de escopo analítico (US-012); contraste shell (RNF-008 Should)
  - Doc: textos das legendas versionados ou no plugin

### TASK-015 — Badge dados fictícios

- **US:** US-018
- **MOD:** MOD-WP-PLUGIN
- **Depends-on:** TASK-007
- **Risco:** Baixo
- **Destino:** PR-015, TEST-015
- **DoD:**
  - Código: `.dsn-badge-fake` visível nas duas páginas
  - Teste: badge presente no load
  - Doc: copy do aviso

### TASK-016 — Estado `error` iframe bloqueado

- **US:** US-020
- **MOD:** MOD-CAROUSEL
- **Depends-on:** TASK-011, TASK-012
- **Risco:** Médio
- **Destino:** PR-016, TEST-016
- **DoD:**
  - Código: `data-state=error` + mensagem; sem expor ES; layout sem scroll
  - Teste: simular framing bloqueado (TEST-020 / UC-06)
  - Doc: comportamento UC-06

### TASK-017 — Estado `empty` dado ausente

- **US:** US-021
- **MOD:** MOD-CAROUSEL
- **Depends-on:** TASK-008, TASK-003
- **Risco:** Médio
- **Destino:** PR-017, TEST-017
- **DoD:**
  - Código: `data-state=empty` + mensagem; carrossel navegável
  - Teste: slide sem dado (TEST-021 / UC-07)
  - Doc: comportamento UC-07

### TASK-018 — Validação catálogos 15 temas / 4 plataformas

- **US:** US-010, US-011
- **MOD:** MOD-SEED, MOD-ES
- **Depends-on:** TASK-003
- **Risco:** Baixo
- **Destino:** PR-018, TEST-018
- **DoD:**
  - Código: assert/script de validação dos valores de `theme` e `platform` no índice
  - Teste: listas exatas dos catálogos
  - Doc: referência aos slugs do schema

### TASK-019 — Auth embeds produção (adiada)

- **US:** US-019
- **MOD:** —
- **Depends-on:** nenhuma
- **Risco:** — (Won't)
- **Destino:** PR-019 (cancelado/placeholder), TEST-019 (N/A)
- **DoD:**
  - Registro explícito “Won’t / fora do incremento” neste backlog e no README do projeto
  - Sem implementação de auth de embeds em produção neste incremento
  - Demo local permanece sem auth de embeds

### TASK-020 — Smoke E2E compose + embeds + carrossel

- **US:** US-003, US-006, US-007
- **MOD:** todos
- **Depends-on:** TASK-013, TASK-016, TASK-017
- **Risco:** Alto (integração)
- **Destino:** PR-020, TEST-020
- **DoD:**
  - Código: checklist/script de smoke (compose up → WP → 2 páginas → embeds)
  - Teste: carrossel + Kibana + Shiny sem framing error; estados error/empty exercitados
  - Doc: passo a passo do smoke

---

## Cobertura US → TASK (100%)

| US | TASK |
|----|------|
| US-001 | TASK-006, TASK-007 |
| US-002 | TASK-006, TASK-007 |
| US-003 | TASK-008, TASK-020 |
| US-004 | TASK-009 |
| US-005 | TASK-010 |
| US-006 | TASK-004, TASK-011, TASK-020 |
| US-007 | TASK-005, TASK-012, TASK-020 |
| US-008 | TASK-013 |
| US-009 | TASK-001, TASK-002, TASK-003 |
| US-010 | TASK-002, TASK-018 |
| US-011 | TASK-002, TASK-018 |
| US-012 | TASK-014 |
| US-013 | TASK-007 |
| US-014 | TASK-008 |
| US-015 | TASK-009, TASK-010 |
| US-016 | TASK-014 |
| US-017 | TASK-003 |
| US-018 | TASK-015 |
| US-019 | TASK-019 |
| US-020 | TASK-016 |
| US-021 | TASK-017 |

**Resultado:** 21/21 US decompostas.

---

## Caminho crítico (resumo)

`TASK-001 → TASK-002 → TASK-003 → TASK-004 → TASK-011 → TASK-013 → TASK-020`

Detalhe e DAG completo: [grafo-dependencias.md](./grafo-dependencias.md).

## Critérios de conclusão

- [x] 100% das US decompostas
- [x] Grafo sem ciclos (ver grafo)
- [x] Caminho crítico identificado

## Próximo passo

Executar **TASK-001** (Compose/smoke base).
