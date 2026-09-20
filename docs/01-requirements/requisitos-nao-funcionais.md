# DSN-DASH — Requisitos Não Funcionais (RNF)

| Campo | Valor |
|-------|-------|
| Projeto | DSN-DASH |
| Fase MEGA | Especificação |
| Autoridade | Este documento **substitui como autoridade** os RNF preliminares em [docs/00-discovery/requisitos-nao-funcionais.md](../00-discovery/requisitos-nao-funcionais.md) |
| Origem | briefing.md + discovery RNF + premissas-riscos |
| Destino | SPEC-*, US-* |
| Data | 2026-09-20 |

**Regra:** cada RNF possui **métrica mensurável**. Descreve **O QUE** medir/garantir, não **COMO** implementar.

---

## Índice MoSCoW

| ID | Título | Prioridade |
|----|--------|------------|
| RNF-001 | Tempo de troca de slide | Must |
| RNF-002 | Ausência de scroll vertical no host | Must |
| RNF-003 | Tempo até primeiro embed útil | Must |
| RNF-004 | Compatibilidade de iframe (sem erro de framing) | Must |
| RNF-005 | Homogeneidade visual mensurável | Must |
| RNF-006 | Carrossel operável por teclado | Must |
| RNF-007 | title em 100% dos iframes | Must |
| RNF-008 | Contraste WCAG 2.1 AA no shell | Should |
| RNF-009 | Elasticsearch inacessível ao browser | Must |
| RNF-010 | Seed sem PII real | Must |
| RNF-011 | Framing com allowlist (sem `*` em produção) | Must |
| RNF-012 | Exatamente duas rotas principais | Must |

---

## Catálogo

### RNF-001 — Tempo de troca de slide

- **Descrição:** A troca de slide no carrossel (lado host) deve ser rápida o suficiente para não prejudicar a exploração.
- **Prioridade:** Must
- **Métrica:** Duração da transição host (início do comando → fim da animação/atualização de estado do slide) **&lt; 300 ms**.
- **Origem discovery:** RNF-001 (preliminar); briefing REQ-003
- **Destino:** SPEC-101, US-101
- **Verificação:** Cronômetro de performance (DevTools Performance / mark) em 10 trocas consecutivas; mediana &lt; 300 ms.

### RNF-002 — Ausência de scroll vertical no host

- **Descrição:** A página-host não deve apresentar scroll vertical no viewport alvo.
- **Prioridade:** Must
- **Métrica:** Overflow vertical do `document`/`body` da página-host = **0** nos viewports **1366×768** e **1920×1080** (desktop), em ambas as páginas, com qualquer slide ativo.
- **Origem discovery:** RNF-001, RNF-002; briefing R-01
- **Destino:** SPEC-102, US-102
- **Verificação:** `scrollHeight <= clientHeight` (ou equivalente) nos dois viewports; sem barra de rolagem vertical visível.

### RNF-003 — Tempo até primeiro embed útil

- **Descrição:** O primeiro gráfico embutido do slide inicial deve tornar-se visível em tempo aceitável em demo local.
- **Prioridade:** Must
- **Métrica:** Conteúdo do iframe do slide inicial **visível em &lt; 5 s** após o carregamento da página, em ambiente local (rede local / Docker na mesma máquina).
- **Origem discovery:** RNF-016 (TBD fechado aqui)
- **Destino:** SPEC-103, US-103
- **Verificação:** Medir do `load` da página-host até o primeiro paint útil do conteúdo do iframe (ou ausência de estado “vazio/erro”).

### RNF-004 — Compatibilidade de iframe

- **Descrição:** Embeds Elasticsearch/Kibana e R/Shiny devem carregar sem bloqueio de framing.
- **Prioridade:** Must
- **Métrica:** **0** erros de framing no console do browser relacionados a `X-Frame-Options` ou `frame-ancestors` ao carregar pelo menos um embed ES/Kibana e um embed R/Shiny em cada página.
- **Origem discovery:** RNF-007; riscos RK-01, RK-02
- **Destino:** SPEC-104, US-104
- **Verificação:** Console limpo quanto a framing; iframe renderiza conteúdo (não página em branco por recusa).

### RNF-005 — Homogeneidade visual mensurável

- **Descrição:** Embeds de origens distintas devem seguir o mesmo sistema visual do painel.
- **Prioridade:** Must
- **Métrica (checklist — 100% itens):**
  1. Mesma paleta com **≥ 4 tokens** de cor compartilhados entre shell e embeds;
  2. Mesma **família tipográfica** do shell aplicada (ou espelhada) nos embeds;
  3. Diferença de **padding externo** do iframe entre origens Kibana e Shiny **≤ 8 px** (em cada lado medido).
- **Origem discovery:** RNF-004; briefing REQ-006
- **Destino:** SPEC-105, US-105
- **Verificação:** Inspeção visual + medição de padding; registro do checklist por página.

### RNF-006 — Carrossel operável por teclado

- **Descrição:** Controles do carrossel devem ser utilizáveis sem mouse.
- **Prioridade:** Must
- **Métrica:** **100%** dos controles de avançar/voltar (e foco no indicador, se interativo) operáveis via teclado (Tab + Enter/Espaço e/ou setas); foco visível em todo controle focado.
- **Origem discovery:** RNF-020
- **Destino:** SPEC-106, US-106
- **Verificação:** Percurso apenas por teclado pelos 4 slides em cada página.

### RNF-007 — title em iframes

- **Descrição:** Todo iframe de visualização deve possuir descrição acessível.
- **Prioridade:** Must
- **Métrica:** **100%** dos elementos `iframe` do painel com atributo `title` não vazio.
- **Origem discovery:** RNF-018
- **Destino:** SPEC-107, US-107
- **Verificação:** Auditoria DOM / checklist automatizado.

### RNF-008 — Contraste do texto do shell

- **Descrição:** Texto do shell WordPress (títulos, legendas, navegação) deve ser legível.
- **Prioridade:** Should
- **Métrica:** Contraste do texto de corpo do host **≥ 4,5:1** (WCAG 2.1 nível AA); textos grandes (≥18 pt / 14 pt bold) ≥ 3:1.
- **Origem discovery:** RNF-019
- **Destino:** SPEC-108, US-108
- **Verificação:** Ferramenta de contraste (axe, Lighthouse ou equivalente) nas duas páginas.

### RNF-009 — Elasticsearch inacessível ao browser

- **Descrição:** O browser do usuário final não deve acessar a API/porta do Elasticsearch diretamente.
- **Prioridade:** Must
- **Métrica:** Tentativa de conexão do browser à API/porta do ES resulta em **falha de acesso** (recusa/timeout/unreachable); **0** endpoints ES expostos publicamente ao cliente do painel.
- **Origem discovery:** RNF-013; H-07; RK-04
- **Destino:** SPEC-109, US-109
- **Verificação:** Teste de rede a partir do contexto do usuário; inspeção de requests do painel (nenhuma chamada direta ao ES).

### RNF-010 — Seed sem PII real

- **Descrição:** Datasets de demo não contêm informações pessoais reais.
- **Prioridade:** Must
- **Métrica:** **0** registros com PII real; dataset marcado/rotulado como fictício.
- **Origem discovery:** RNF-009; briefing R-03
- **Destino:** SPEC-110, US-110
- **Verificação:** Revisão amostral do seed + declaração no artefato de dados.

### RNF-011 — Framing com allowlist

- **Descrição:** Políticas de framing devem listar origens explícitas.
- **Prioridade:** Must
- **Métrica:** Em ambiente de demonstração alinhado a produção e em produção: `frame-ancestors` (ou equivalente) com **origens explícitas**; uso de `*` em `frame-ancestors` = **0** ocorrências em produção.
- **Origem discovery:** RNF-014; briefing REQ-012
- **Destino:** SPEC-111, US-111
- **Verificação:** Inspeção de headers HTTP das respostas dos serviços embutidos.

### RNF-012 — Exatamente duas rotas principais

- **Descrição:** O produto de painel limita-se a duas páginas/rotas principais.
- **Prioridade:** Must
- **Métrica:** Contagem de rotas/páginas principais do painel = **2** (Por Tema, Por Plataforma).
- **Origem discovery:** RNF-002; briefing R-02
- **Destino:** SPEC-112, US-112
- **Verificação:** Inventário de navegação do produto; ausência de terceira rota principal de análise.

---

## Mapeamento discovery → RNF formal

| Discovery (preliminar) | Formal (este doc) |
|------------------------|-------------------|
| RNF-001 (carrossel/sem scroll) | RNF-001, RNF-002 |
| RNF-002 (2 páginas) | RNF-012 |
| RNF-004 (homogeneidade) | RNF-005 |
| RNF-007 (headers frame) | RNF-004, RNF-011 |
| RNF-009 / RNF-010 (seed) | RNF-010 (+ RF-009/017) |
| RNF-013 (ES fechado) | RNF-009 |
| RNF-016 (performance TBD) | RNF-003 (5 s) |
| RNF-018 / RNF-020 (a11y) | RNF-007, RNF-006 |
| RNF-019 (contraste) | RNF-008 |

---

## Critérios de cobertura

- [x] Performance (RNF-001, RNF-003)
- [x] UX / viewport (RNF-002, RNF-012)
- [x] Compatibilidade iframe (RNF-004, RNF-011)
- [x] Acessibilidade (RNF-006, RNF-007, RNF-008)

## Próximo passo

Incorporar métricas nos critérios de aceite das SPEC/US correspondentes (SPEC-101..112).
