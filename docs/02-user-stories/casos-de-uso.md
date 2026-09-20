# DSN-DASH — Casos de Uso

| Campo | Valor |
|-------|-------|
| Projeto | DSN-DASH |
| Fase MEGA | Especificação detalhada |
| Origem | [backlog.md](./backlog.md), RF/RNF Etapa 1 |
| Destino | TEST-* |
| Data | 2026-09-20 |

**Atores:** P1 Analista de desinformação · P2 Cliente/demonstração · P3 Admin WP

---

## Índice

| ID | Caso de uso | Atores | Tipo |
|----|-------------|--------|------|
| UC-01 | Explorar painel Por Tema | P1, P2 | Feliz |
| UC-02 | Explorar painel Por Plataforma | P1, P2 | Feliz |
| UC-03 | Percorrer carrossel (4 slides) | P1, P2 | Feliz |
| UC-04 | Alternar entre Tema e Plataforma | P1, P2 | Feliz |
| UC-05 | Visualizar embeds Kibana e Shiny | P1, P2 | Feliz → UC-06 |
| UC-06 | Tratar iframe bloqueado | P1, P2, P3 | Exceção |
| UC-07 | Tratar dado/visualização ausente | P1, P2, P3 | Exceção |
| UC-08 | Preparar/reaplicar seed fictício | P3 | Feliz + alt. |
| UC-09 | Conduzir demonstração ao cliente | P2, P1 | Feliz |

---

## UC-01 — Explorar painel Por Tema

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Visualizar a propagação de desinformação no eixo tema |
| **Atores** | P1, P2 |
| **Pré-condições** | Painel disponível; seed carregado (US-009); catálogo de temas (US-010) |
| **Pós-condições** | Usuário vê a página Por Tema com carrossel e conteúdo do eixo tema |
| **US** | US-001, US-003, US-004, US-010, US-015, US-016 |
| **TEST** | TEST-001, TEST-UC-01 |

### Fluxo principal

1. Ator acessa o painel DSN-DASH.
2. Ator seleciona a entrada **Por Tema**.
3. Sistema apresenta a página Por Tema (distinta de Por Plataforma).
4. Sistema exibe o primeiro slide do carrossel no viewport, sem scroll vertical no host.
5. Ator lê legenda curta e visualiza o gráfico do slide.

### Fluxos alternativos

- **A1:** Ator chega via link direto à URL/rota Por Tema → continua no passo 3.

### Exceções

- Encaminha para **UC-06** se embed do slide falhar por framing.
- Encaminha para **UC-07** se dado/visualização do slide estiver ausente.

---

## UC-02 — Explorar painel Por Plataforma

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Visualizar a propagação no eixo plataforma |
| **Atores** | P1, P2 |
| **Pré-condições** | Painel disponível; seed carregado; catálogo de plataformas (US-011) |
| **Pós-condições** | Usuário vê a página Por Plataforma com carrossel do eixo plataforma |
| **US** | US-002, US-003, US-005, US-011, US-015, US-016 |
| **TEST** | TEST-002, TEST-UC-02 |

### Fluxo principal

1. Ator acessa o painel.
2. Ator seleciona **Por Plataforma**.
3. Sistema apresenta a página Por Plataforma.
4. Sistema exibe o primeiro slide sem scroll vertical no host.
5. Ator lê legenda e gráfico alinhados ao eixo plataforma.

### Exceções

- **UC-06** / **UC-07** conforme falha de embed ou dado.

---

## UC-03 — Percorrer carrossel (4 slides)

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Navegar os 4 slides de uma página principal |
| **Atores** | P1, P2 |
| **Pré-condições** | Ator está em UC-01 ou UC-02 |
| **Pós-condições** | Ator visitou os 4 slides; indicador reflete posição final |
| **US** | US-003, US-004, US-005, US-014 |
| **TEST** | TEST-003, TEST-014, TEST-UC-03 |

### Fluxo principal

1. Ator vê o slide atual e o indicador de posição (ex.: 1 de 4).
2. Ator aciona **avançar** (clique ou teclado).
3. Sistema troca o slide em &lt; 300 ms no host e atualiza o indicador.
4. Ator repete até o slide 4.
5. Ator pode **voltar** até o slide 1; indicador permanece consistente.

### Fluxos alternativos

- **A1:** Navegação apenas por teclado (Tab/Enter ou setas) — 100% dos controles operáveis; foco visível.

### Exceções

- Slide sem conteúdo → **UC-07**.
- Embed bloqueado no slide → **UC-06**.

---

## UC-04 — Alternar entre Tema e Plataforma

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Trocar o eixo de análise pela navegação do produto |
| **Atores** | P1, P2 |
| **Pré-condições** | Ambas as páginas existem (US-001, US-002) |
| **Pós-condições** | Ator está na outra página principal; apenas 2 rotas principais no produto |
| **US** | US-013, US-001, US-002 |
| **TEST** | TEST-013, TEST-UC-04 |

### Fluxo principal

1. Ator está em Por Tema (ou Por Plataforma).
2. Ator aciona o controle de navegação para a outra página.
3. Sistema apresenta a página destino com seu carrossel no slide inicial (ou estado padrão definido).

### Exceções

- Nenhuma específica além de falhas gerais de carregamento de página (tratar como erro de disponibilidade do host).

---

## UC-05 — Visualizar embeds Kibana e Shiny

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Ver gráficos das duas origens embutidos no painel |
| **Atores** | P1, P2 |
| **Pré-condições** | Seed ok; serviços de visualização configurados para framing; ator em página com slides |
| **Pós-condições** | Pelo menos um embed Kibana e um Shiny visíveis por página ao longo do carrossel; aparência homogênea |
| **US** | US-006, US-007, US-008 |
| **TEST** | TEST-006, TEST-007, TEST-008, TEST-UC-05 |

### Fluxo principal

1. Ator percorre os slides de uma página (UC-03).
2. Sistema renderiza embed Kibana em ao menos um slide (iframe com `title`).
3. Sistema renderiza embed Shiny em ao menos um slide (iframe com `title`).
4. No slide inicial com embed, conteúdo útil aparece em &lt; 5 s (ambiente local).
5. Ator percebe homogeneidade visual (paleta, tipografia, padding) entre origens.
6. Browser do ator **não** acessa a API do Elasticsearch diretamente.

### Exceções

- Framing recusado → **UC-06**.
- Conteúdo do embed vazio por falta de dado → **UC-07**.

---

## UC-06 — Tratar iframe bloqueado

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Informar falha de framing sem quebrar UX do host |
| **Atores** | P1, P2 (percebem); P3 (corrige config) |
| **Pré-condições** | Slide com embed; serviço filho ou proxy bloqueia framing |
| **Pós-condições** | Mensagem clara no host; layout estável; ES não exposto; P3 pode corrigir allowlist |
| **US** | US-020 (; RF-006, RF-007, RNF-004, RNF-011) |
| **TEST** | TEST-020, TEST-UC-06 |

### Fluxo principal (exceção)

1. Ator navega até o slide cujo embed está bloqueado.
2. Browser impede a renderização do iframe (X-Frame-Options / frame-ancestors).
3. Sistema host detecta falha ou estado vazio do embed e exibe **mensagem compreensível** (ex.: “Visualização temporariamente indisponível”).
4. Carrossel permanece navegável; página-host **sem** scroll vertical indesejado.
5. Sistema **não** oferece acesso direto ao Elasticsearch como alternativa.

### Fluxo do Admin (recuperação)

6. P3 verifica headers (`frame-ancestors` com origens explícitas; sem `*` em produção).
7. P3 corrige configuração do serviço/proxy.
8. Retorno a **UC-05** com embeds ok.

---

## UC-07 — Tratar dado/visualização ausente

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Sinalizar ausência de dado ou gráfico sem “branco silencioso” |
| **Atores** | P1, P2 (percebem); P3 (reaplica seed se necessário) |
| **Pré-condições** | Slide ativo cuja fonte de dado/visualização esperada está ausente |
| **Pós-condições** | Estado/mensagem de indisponibilidade; carrossel utilizável; layout intacto |
| **US** | US-021 (; RF-009, RF-004, RF-005) |
| **TEST** | TEST-021, TEST-UC-07 |

### Fluxo principal (exceção)

1. Ator ativa um slide sem dado ou sem visualização carregável.
2. Sistema exibe estado/mensagem de **dado indisponível** no host (linguagem simples).
3. Controles do carrossel continuam funcionando (avançar/voltar/indicador).
4. Layout do host não introduz scroll vertical.

### Fluxo do Admin (recuperação)

5. P3 verifica seed (UC-08) e reaplica se a ausência for falha de carga.
6. Retorno ao fluxo feliz do slide.

---

## UC-08 — Preparar/reaplicar seed fictício

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Disponibilizar dados fictícios dimensionais e reprodutíveis |
| **Atores** | P3 |
| **Pré-condições** | Artefato/procedimento de seed versionado disponível |
| **Pós-condições** | Domínio 4 plataformas × 15 temas × 27 UFs × 2021–2024 disponível; sem PII real |
| **US** | US-009, US-017, US-010, US-011 |
| **TEST** | TEST-009, TEST-017, TEST-UC-08 |

### Fluxo principal

1. P3 obtém o artefato/procedimento versionado do seed.
2. P3 executa a carga do seed no ambiente de demo.
3. Sistema disponibiliza dimensões do domínio.
4. P3 confirma ausência de PII real e rótulo/caráter fictício dos dados.

### Fluxos alternativos / exceções

- **E1 — Falha de carga:** sistema ou procedimento reporta erro; P3 corrige e repete do passo 2; páginas podem cair em UC-07 até sucesso.
- **E2 — Seed parcial:** dimensões faltantes → tratar como não conformidade de US-009; não liberar demo completa.

---

## UC-09 — Conduzir demonstração ao cliente

| Campo | Conteúdo |
|-------|----------|
| **Objetivo** | Percorrer o painel em demo rápida e compreensível |
| **Atores** | P2 (audiência), P1 (pode conduzir) |
| **Pré-condições** | Seed ok; páginas e embeds no fluxo feliz; indicação de dados fictícios (US-018, Could) |
| **Pós-condições** | Audiência viu ambos os eixos, carrossel e gráficos homogêneos sem ML |
| **US** | US-012, US-013, US-016, US-018, US-008 |
| **TEST** | TEST-UC-09, TEST-012, TEST-018 |

### Fluxo principal

1. Condutor abre Por Tema (UC-01) e destaca aviso de dados fictícios, se presente.
2. Percorre 4 slides (UC-03), lendo legendas curtas.
3. Alterna para Por Plataforma (UC-04).
4. Percorre slides e aponta embeds Kibana e Shiny (UC-05) e homogeneidade.
5. Reforça que análises são apenas descritivas (sem ML).

### Exceções

- Durante a demo, falha de iframe → **UC-06** (mensagem clara; não improvisar acesso ao ES).
- Slide vazio → **UC-07**.

---

## Rastreabilidade UC → US → TEST

| UC | US principais | TEST |
|----|---------------|------|
| UC-01 | US-001, US-004 | TEST-UC-01, TEST-001 |
| UC-02 | US-002, US-005 | TEST-UC-02, TEST-002 |
| UC-03 | US-003, US-014 | TEST-UC-03, TEST-014 |
| UC-04 | US-013 | TEST-UC-04, TEST-013 |
| UC-05 | US-006, US-007, US-008 | TEST-UC-05 |
| UC-06 | US-020 | TEST-UC-06, TEST-020 |
| UC-07 | US-021 | TEST-UC-07, TEST-021 |
| UC-08 | US-009, US-017 | TEST-UC-08 |
| UC-09 | US-012, US-018 | TEST-UC-09 |

---

## Critérios de conclusão

- [x] Fluxos felizes cobertos (UC-01..05, UC-08, UC-09)
- [x] Exceção iframe bloqueado (UC-06)
- [x] Exceção dado ausente (UC-07)
- [x] Ligação a US e TEST-*

## Próximo passo

Quebra técnica **TASK-*** e especificação de casos de teste **TEST-*** (priorizar TEST-020 e TEST-021).
