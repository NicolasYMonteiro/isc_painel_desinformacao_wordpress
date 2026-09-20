# DSN-DASH — Briefing de Descoberta

| Campo | Valor |
|-------|-------|
| Projeto | DSN-DASH (Dashboard de análise de propagação de desinformação) |
| Fase MEGA | Descoberta |
| Repositório | `isc_painel_desinformacao_wordpress` (greenfield) |
| Origem | Nenhuma (partida do zero) |
| Destino | REQ-001..N (Etapa 1 — Especificação de Requisitos) |
| Data | 2026-09-20 |

---

## 1. Resumo executivo

O DSN-DASH é um painel web para **visualizar e explorar** a propagação de desinformação de forma acessível a pesquisadores (internos e externos) e ao **público geral**. A interface WordPress concentra **duas páginas** (Por Tema e Por Plataforma), **sem scroll vertical** na página-host, com navegação por **carrossel lateral**. Gráficos vindos de Kibana (Elasticsearch) e de R (Shiny/ggplot2) devem parecer **homogêneos**. Nesta fase não há dados reais: apenas **seed fictício**. Análises limitam-se a descrições e agregações simples — **sem machine learning nem estatística complexa**.

A stack candidata (WordPress + Elasticsearch/Kibana via iframe + R/Shiny) é **hipótese de arquitetura**, não decisão fechada. Versões de bibliotecas e smoke test Docker ficam abertos. Taxonomias de Tema e Plataforma permanecem **hipótese até a Etapa 1**.

---

## 2. Problema

Há necessidade de um painel único, legível e navegável, que permita observar padrões de propagação de desinformação por **tema** e por **plataforma**, sem exigir conhecimento técnico avançado do usuário. Hoje o repositório não possui código nem baseline de produto; o risco é iniciar a especificação sem escopo, restrições de UX e riscos de integração (iframe/CSP) explicitados.

---

## 3. Público-alvo

| Segmento | Necessidade | Implicação de produto |
|----------|-------------|------------------------|
| Pesquisadores internos | Explorar indicadores e comparar eixos Tema/Plataforma | Gráficos claros, filtros simples, linguagem consistente |
| Pesquisadores externos | Consumir o painel sem onboarding pesado | Mesma UX; sem jargão estatístico avançado |
| Público geral | Compreender o essencial da propagação | Textos curtos, agregações básicas, zero ML |

**Delimitação analítica confirmada:** apenas análise descritiva/exploratória dos dados. Fora de escopo: modelos preditivos, ML, inferência estatística avançada, técnicas que exijam interpretação especializada.

---

## 4. Valor esperado

- **Clareza:** um lugar para ver “o que se propaga” por tema e por plataforma.
- **Acessibilidade cognitiva:** conteúdo compreensível para público geral e útil para pesquisa.
- **Consistência visual:** gráficos de origens distintas (Kibana e Shiny) percebidos como parte do mesmo produto.
- **Demo segura:** seed fictício permite validar UX e integração sem dados reais/PII.

---

## 5. Escopo funcional preliminar

### 5.1 Dentro do escopo (descoberta → requisitos)

| Item | Descrição | Status |
|------|-----------|--------|
| Duas páginas | **Por Tema** e **Por Plataforma** | Restrição confirmada |
| Sem scroll na página-host | Viewport único; conteúdo adicional via **carrossel lateral** | Restrição confirmada |
| Embeds de visualização | Kibana (iframe) e Shiny/ggplot2 (iframe ou equivalente) | Hipótese de arquitetura |
| Dados | Seed fictício para demos e desenvolvimento | Hipótese operacional |
| Linguagem | Análise simples, não especializada | Confirmado |

### 5.2 Fora de escopo (explícito)

- Machine learning e estatística complexa
- Mais de duas páginas/rotas principais
- Scroll vertical na página-host como padrão de navegação
- Dados reais / PII em ambiente de discovery/demo
- Escolha e pin de versões finais de bibliotecas (somente viabilidade nesta fase)
- Fechamento de taxonomias Tema/Plataforma (hipótese aberta até Etapa 1)

---

## 6. Stack candidata (hipótese)

```
Browser → WordPress (host / carrossel)
            ├── iframe → Kibana → Elasticsearch
            └── iframe → Shiny (R / ggplot2)
```

| Camada | Papel candidato | Classificação |
|--------|-----------------|---------------|
| WordPress | Shell da UI, páginas Tema/Plataforma, carrossel, CSS de homogeneidade | Hipótese |
| Elasticsearch + Kibana | Armazenamento/consulta e dashboards embutidos | Hipótese |
| R + Shiny (+ ggplot2) | Visualizações complementares embutidas | Hipótese |
| Docker Compose | Ambiente local unificado | Hipótese (validação documental; smoke test aberto) |

Detalhes de premissas, CORS/CSP/`X-Frame-Options` e riscos: ver [premissas-riscos.md](./premissas-riscos.md).  
RNFs preliminares: ver [requisitos-nao-funcionais.md](./requisitos-nao-funcionais.md).

---

## 7. Restrições técnicas críticas (mapa)

| Restrição | Impacto |
|-----------|---------|
| Página-host sem scroll | Layout e altura de iframes devem caber no viewport; overflow interno dos embeds é risco |
| Carrossel lateral obrigatório | Navegação horizontal entre “painéis/slides”; estado e acessibilidade a especificar na Etapa 1 |
| Homogeneidade visual multi-origem | Tema WP + theming Shiny + opções de embed Kibana; chrome nativo do Kibana pode vazar |
| Embeds cross-origin | Dependem de `frame-ancestors` / ausência de `X-Frame-Options: SAMEORIGIN` nos serviços filhos; CSP `frame-src` no WP |
| Sem dados reais | Seed fictício; índices e datasets de demonstração |

---

## 8. Rastreabilidade — placeholders REQ

Itens abaixo devem ser refinados e formalizados na **Etapa 1**. IDs reservados a partir deste briefing:

| ID | Tema (rascunho) | Origem neste briefing |
|----|-----------------|------------------------|
| REQ-001 | Página Por Tema | §5.1 |
| REQ-002 | Página Por Plataforma | §5.1 |
| REQ-003 | Navegação sem scroll + carrossel lateral | §5.1, §7 |
| REQ-004 | Embed Kibana via iframe | §6 |
| REQ-005 | Embed Shiny/ggplot2 via iframe | §6 |
| REQ-006 | Homogeneidade visual entre fontes de gráfico | §5.1, §7 |
| REQ-007 | Seed de dados fictícios | §5.1 |
| REQ-008 | Linguagem e análises acessíveis (sem ML/estatística complexa) | §3 |
| REQ-009 | Taxonomia de Temas (a definir) | Hipótese aberta |
| REQ-010 | Taxonomia de Plataformas (a definir) | Hipótese aberta |
| REQ-011 | Ambiente local Docker Compose | §6; premissas |
| REQ-012 | Configuração de headers de frame (CSP / XFO) nos embeds | §7; premissas-riscos |

RNFs associados: RNF-001..N em [requisitos-nao-funcionais.md](./requisitos-nao-funcionais.md).

---

## 9. Critérios de conclusão desta discovery

- [x] Problema, público-alvo e valor descritos
- [x] Restrições técnicas (iframe/CSP/CORS) mapeadas (detalhe em premissas-riscos)
- [x] Riscos classificados alto/médio/baixo (em premissas-riscos)
- [x] Premissas de ambiente local (Docker) registradas com validação documental; smoke test como premissa aberta

---

## 10. Premissas abertas (lista)

1. Taxonomias concretas de **Tema** e **Plataforma**
2. Versões finais de WordPress, Elastic Stack, R/Shiny e imagens Docker
3. Smoke test local (`docker compose up`) da topologia proposta
4. Modelo de autenticação dos embeds Kibana em ambiente público vs. restrito
5. Métricas numéricas de performance (tempo de carga dos iframes)
6. Decisão se Shiny será Shiny Server, ShinyProxy ou container mínimo
7. Se o reverse proxy fará same-origin dos embeds (mitiga CSP) ou permanecerá multi-origem

---

## 11. Próximo passo

**Etapa 1 — Especificação de Requisitos:** transformar este briefing e os RNFs preliminares em REQ-001..N formalizados (funcionais e não funcionais), fechar ou delimitar taxonomias Tema/Plataforma, e preparar critérios de aceite para a fase de arquitetura/protótipo.
