# DSN-DASH — Relatório QA (Validação)

| Campo | Valor |
|-------|-------|
| Fase MEGA | Validação |
| Data | 2026-09-20 |
| Ambiente | Docker local (WP :8080, ES :9200, Kibana :5601, Shiny :3838) |
| Suite | Playwright + axe-core (`tests/e2e/qa-validation.spec.js`) |
| Regra | Falhas **reportadas**; sem correção nesta fase |
| Destino | BUG-*, DELIVERABLE-QA-001 |

## Resumo executivo

| Indicador | Valor |
|-----------|-------|
| Conformidade Must (RF+RNF aplicáveis) | **~76%** (19/25 Must verificados OK) |
| Critérios verificados | 100% dos RF/RNF do catálogo (incl. Won't/Should) |
| Bugs abertos | **5** (1 Alto, 3 Médios, 1 Baixo) |
| Screenshots | 8 (`docs/06-validation/screenshots/`) |
| E2E Playwright | 6/6 testes estruturais passaram; falhas de produto capturadas como bugs |

---

## Métricas RNF

| RNF | Métrica | Resultado | Status |
|-----|---------|-----------|--------|
| RNF-001 | Troca de slide | 298 ms (tema), 292 ms (plataforma) | **PASS** (&lt; 300 ms) |
| RNF-002 | Sem scroll host 1366×768 / 1920×1080 | `hasScroll=true`; scrollHeight 1567&gt;768 / 1879&gt;1080 | **FAIL** → BUG-001 |
| RNF-003 | 1º embed útil | 2791 ms | **PASS** (&lt; 5 s) |
| RNF-004 | 0 erros framing | `framingHits=[]`; porém CSP/`404`/`TypeError` nos embeds Kibana | **FAIL parcial** → BUG-002 |
| RNF-005 | Tokens + padding | ≥4 tokens cor; padding frames 12px uniforme | **PASS** (host); conteúdo iframe Kibana degradado (BUG-002) |
| RNF-006 | Teclado | Controles focáveis + Enter | **PASS** |
| RNF-007 | `title` iframes | 100% não vazio | **PASS** |
| RNF-008 | Contraste/a11y shell | axe: 1 violação **serious** (listas WP theme) | **FAIL** (Should) → BUG-003 |
| RNF-009 | ES inacessível ao browser | GET `localhost:9200` → **200** | **FAIL** → BUG-004 |
| RNF-010 | Seed sem PII | Validado em seed/catalogos | **PASS** |
| RNF-011 | frame-ancestors allowlist | `kibana.yml` com origem WP explícita | **PASS** (config) |
| RNF-012 | 2 rotas | `/por-tema/`, `/por-plataforma/` | **PASS** |

Fonte: [`metrics.jsonl`](./metrics.jsonl), [`es-exposure.json`](./es-exposure.json), [`homogeneity.json`](./homogeneity.json), [`axe-*.json`](./axe-por-tema.json).

---

## Verificação RF (aceite)

| RF | Resultado | Evidência |
|----|-----------|-----------|
| RF-001 Página Tema | PASS | HTTP 200 + `.dsn-dashboard[data-page]` |
| RF-002 Página Plataforma | PASS | idem |
| RF-003 Carrossel sem scroll | **FAIL** | RNF-002 / BUG-001 |
| RF-004 4 slides Tema | PASS | count=4 + screenshots |
| RF-005 4 slides Plataforma | PASS | count=4 + screenshots |
| RF-006 Embed Kibana | **FAIL** | console 404 + TypeError CSP (BUG-002) |
| RF-007 Embed Shiny | PASS condicional | iframe presente; slides 3–4 renderizam (screenshots maiores) |
| RF-008 Homogeneidade | PASS parcial | tokens host OK; Kibana quebrado reduz homogeneidade real |
| RF-009 Seed dimensional | PASS | 50k docs; aggs 4×15×27×4 |
| RF-010 15 temas | PASS | `validate_catalogs.py` |
| RF-011 4 plataformas | PASS | idem |
| RF-012 Só descritivo | PASS | revisão escopo (sem ML na UI) |
| RF-013 Navegação | PASS | E2E nav Tema↔Plataforma |
| RF-014 Controles/indicador | PASS | prev/next + indicator no DOM |
| RF-015 Eixo alinhado | PASS | captions por página |
| RF-016 Legendas | PASS | caption length &gt; 10 em 8 slides |
| RF-017 Seed reprodutível | PASS | script seed=42 versionado |
| RF-018 Badge fictício | PASS | `.dsn-badge-fake` visível |
| RF-019 Auth prod | N/A Won't | fora do incremento |

---

## Bugs (somente report)

### BUG-001 — Scroll vertical efetivo na página-host
- **Severidade:** Alta (Must RNF-002 / RF-003)
- **Origem:** RNF-002, RF-003, US-003
- **Evidência:** `scrollHeight` 1567 &gt; `clientHeight` 768 (e 1879 &gt; 1080); `hasScroll=true` apesar de `bodyOverflow=hidden`
- **Impacto:** Quebra restrição “sem scroll”; tema WP (header/nav) extrapola viewport 100vh do plugin

### BUG-002 — Embeds Kibana com CSP / 404 / TypeError
- **Severidade:** Alta (Must RF-006 / RNF-004)
- **Origem:** RF-006, US-006, RNF-004
- **Evidência:** [`console-por-tema.json`](./console-por-tema.json) — CSP `script-src`, recursos 404, `Cannot read properties of undefined (reading 'mode')`; `framingHits` vazio (não é XFO, é falha de app Kibana no iframe)
- **Impacto:** Gráficos Kibana não úteis no carrossel; Shiny parece OK

### BUG-003 — Acessibilidade: listas do tema WP (axe serious)
- **Severidade:** Média (Should RNF-008 / a11y)
- **Origem:** RNF-008, axe
- **Evidência:** rule `list` — `.wp-block-page-list` / navigation com filhos `ul` inválidos
- **Impacto:** WCAG 1.3.1 no chrome do tema (fora do shortcode DSN)

### BUG-004 — Elasticsearch exposto ao browser (porta 9200)
- **Severidade:** Alta (Must RNF-009)
- **Origem:** RNF-009, ADR-001
- **Evidência:** [`es-exposure.json`](./es-exposure.json) — `direct.status=200`
- **Impacto:** Viola “ES não acessível pelo browser”; publish deliberado no compose de demo

### BUG-005 — Regressão visual: área de gráfico Kibana vazia/erro
- **Severidade:** Média (UX / RF-008)
- **Origem:** screenshots slides 1–2 vs 3–4
- **Evidência:** PNGs Tema/Plataforma slides 1–2 (~28–30 KB) vs Shiny 3–4 (~36–37 KB); console errors correlatos
- **Impacto:** Carrossel funcional, conteúdo Kibana não entrega valor

---

## Screenshots (DELIVERABLE)

| Arquivo | Página | Slide |
|---------|--------|-------|
| `screenshots/por-tema-slide-1.png` … `4.png` | Por Tema | 1–4 |
| `screenshots/por-plataforma-slide-1.png` … `4.png` | Por Plataforma | 1–4 |

---

## Conformidade

- Must RF aplicáveis (excl. RF-019): **12/14 PASS** (~86%) — falhas RF-003, RF-006  
- Must RNF: **7/11 PASS** (~64%) — falhas RNF-002, RNF-004, RNF-009 (+ RNF-008 Should)  
- **Agregado Must:** **19/25 = 76%**

---

## Critérios de conclusão

- [x] 100% dos critérios de aceite **verificados** (pass ou fail documentado)
- [x] RNF medidos (troca de slide, scroll, first-embed, exposição ES, tokens, axe)
- [x] Rastreabilidade REQ→TEST em [`cobertura-rastreabilidade.csv`](./cobertura-rastreabilidade.csv)

## Próximo passo

Priorizar correção autorizada de **BUG-001** (layout/scroll) e **BUG-002** (embeds Kibana); em seguida **BUG-004** (não publicar ES ou restringir bind). Reexecutar suite E2E após fixes → DELIVERABLE-QA-002.
