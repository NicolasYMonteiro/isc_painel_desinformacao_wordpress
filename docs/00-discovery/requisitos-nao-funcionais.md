# DSN-DASH — Requisitos não funcionais (preliminares)

| Campo | Valor |
|-------|-------|
| Projeto | DSN-DASH |
| Fase | Descoberta |
| Natureza | Preliminares — a formalizar na Etapa 1 |
| Relacionado | [briefing.md](./briefing.md), [premissas-riscos.md](./premissas-riscos.md) |
| Data | 2026-09-20 |

Cada RNF aponta rastreabilidade a placeholders REQ do briefing e/ou a riscos em premissas-riscos. Métricas numéricas (quando “TBD”) serão fechadas na Etapa 1.

---

## Catálogo RNF

### UX e navegação

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-001 | A página-host **não** deve apresentar scroll vertical como meio principal de navegação; o conteúdo adicional é acessível por **carrossel lateral**. | Alta | REQ-003; R-01 |
| RNF-002 | O produto expõe exatamente **duas** páginas/rotas principais: Por Tema e Por Plataforma. | Alta | REQ-001, REQ-002; R-02 |
| RNF-003 | Textos de interface e legendas devem ser compreensíveis por **público geral**, sem jargão de ML ou estatística avançada. | Alta | REQ-008 |

### Visual e homogeneidade

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-004 | Gráficos originados de Kibana e de Shiny/ggplot2 devem apresentar **aparência visual homogênea** (cores, tipografia, densidade, padding) sob o tema do painel. | Alta | REQ-006; RK-05; P-HOMOG |
| RNF-005 | Iframes embutidos devem ocupar área definida pelo layout do viewport (altura/largura consistentes com o carrossel), evitando “quebra” do shell WP. | Alta | REQ-003; RK-06 |

### Integração e embeds

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-006 | Visualizações Kibana e Shiny são entregues via **iframe** (ou mecanismo equivalente de isolamento), sem exposição da API do Elasticsearch ao browser. | Alta | REQ-004, REQ-005; H-07; RK-04 |
| RNF-007 | Serviços embutidos devem publicar headers que permitam framing pela origem do WordPress (`Content-Security-Policy: frame-ancestors` e ausência de XFO bloqueante); o host WP deve permitir as origens em `frame-src` quando CSP estiver ativo. | Alta | REQ-012; RK-01, RK-02, RK-03 |
| RNF-008 | A arquitetura de front **não** deve depender de CORS para *exibir* os gráficos; chamadas `fetch` cross-origin do tema WP para ES/Shiny são desencorajadas. | Média | P-CORS; F-05 |

### Dados

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-009 | Ambientes de discovery/demo usam **apenas seed fictício**; sem PII nem dados reais de produção. | Alta | REQ-007; R-03 |
| RNF-010 | O seed deve ser reprodutível (documentado/versionável) para recriar demos locais. | Média | REQ-007; P-SEED |

### Ambiente e operação

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-011 | Desenvolvimento local deve ser possível via **Docker Compose** reunindo os serviços da topologia candidata (WP, DB, ES, Kibana, Shiny). | Alta | REQ-011; P-ENV |
| RNF-012 | Versões de imagens e bibliotecas serão **fixadas em etapa posterior**; nesta discovery apenas a viabilidade da topologia é assumida. | Alta | P-VER; R-06 |
| RNF-013 | Elasticsearch não deve ser acessível publicamente a partir do browser do usuário final. | Alta | H-07; RK-04 |

### Segurança

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-014 | Configuração de framing deve ser **explícita e mínima** (allowlist de origens), evitando `*` em produção. | Alta | REQ-012; RK-01, RK-02 |
| RNF-015 | Política de autenticação dos embeds Kibana (público vs autenticado) deve ser decidida antes de produção; demo local pode operar sem auth. | Média | RK-07 |

### Performance

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-016 | Tempo percebido de carga dos embeds no viewport inicial deve ser **aceitável** para demo e uso exploratório. Métrica numérica: **TBD na Etapa 1**. | Média | Premissa aberta §briefing |
| RNF-017 | A stack Docker local deve documentar requisitos mínimos de máquina; degradação por falta de RAM é risco conhecido (mitigar com perfis compose se necessário). | Baixa | RK-08 |

### Acessibilidade (preliminar)

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-018 | Todo iframe deve possuir atributo `title` descritivo. | Média | Boas práticas a11y |
| RNF-019 | Informação crítica nos gráficos não deve depender **somente** de cor; contraste de texto do shell WP deve ser legível. | Média | Público geral |
| RNF-020 | Controles do carrossel devem ser operáveis por teclado (detalhamento na Etapa 1). | Média | REQ-003 |

### Escopo analítico (restrição de qualidade/produto)

| ID | Requisito | Prioridade | Rastreabilidade |
|----|-----------|------------|-----------------|
| RNF-021 | O painel limita-se a **descrições e agregações simples**; não inclui ML, modelos preditivos ou estatística complexa como capacidade do produto. | Alta | REQ-008; R-04 |

> Nota: RNF-021 funciona como restrição de escopo de qualidade/produto (não-funcional no sentido de “o sistema não deve oferecer X”), alinhada ao briefing.

---

## Matriz resumida RNF → REQ

| RNF | REQ relacionados |
|-----|------------------|
| RNF-001, RNF-005, RNF-020 | REQ-003 |
| RNF-002 | REQ-001, REQ-002 |
| RNF-003, RNF-021 | REQ-008 |
| RNF-004 | REQ-006 |
| RNF-006 | REQ-004, REQ-005 |
| RNF-007, RNF-014 | REQ-012 |
| RNF-009, RNF-010 | REQ-007 |
| RNF-011, RNF-012 | REQ-011 |
| RNF-008, RNF-013, RNF-015–019 | Apoio / Etapa 1 |

---

## Itens TBD para a Etapa 1

1. Limiar numérico de RNF-016 (ex.: LCP / tempo até primeiro gráfico útil).
2. Critérios objetivos de “homogeneidade” (RNF-004): checklist visual ou tokens.
3. Comportamento exato do carrossel (RNF-001, RNF-020): slides por página, foco, anúncios ARIA.
4. Taxonomias que impactam filtros e rótulos (REQ-009, REQ-010) — ainda hipótese.
5. Decisão de auth (RNF-015) e same-origin via proxy vs multi-origem.

---

## Próximo passo

Formalizar estes RNF como requisitos versionados na **Etapa 1 — Especificação de Requisitos**, com critérios de aceite testáveis e vínculo aos REQ-001..N.
