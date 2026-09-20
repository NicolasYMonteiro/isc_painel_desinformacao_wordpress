# DSN-DASH — Requisitos Funcionais (RF)

| Campo | Valor |
|-------|-------|
| Projeto | DSN-DASH |
| Fase MEGA | Especificação |
| Origem | [docs/00-discovery/briefing.md](../00-discovery/briefing.md) |
| Destino | SPEC-*, US-* (próxima fase) |
| Data | 2026-09-20 |

**Regra:** descreve **O QUE** o sistema deve fazer, não **COMO** implementar.

---

## Domínio de dados (fechado nesta especificação)

| Dimensão | Valores |
|----------|---------|
| Plataformas (4) | WhatsApp, Facebook, Instagram, YouTube |
| Temas (15) | eleição, governo, vacinas, saúde, educação, economia, segurança, meio_ambiente, religião, gênero, imigração, ciência, mídia, justiça, outros |
| Temporal | Anos 2021, 2022, 2023, 2024 |
| Geográfico | 27 Unidades Federativas (UFs) do Brasil |

**N slides/gráficos:** 8 no total — 4 no carrossel da página Por Tema + 4 no carrossel da página Por Plataforma; cada página inclui pelo menos um embed Elasticsearch/Kibana e um embed R/Shiny.

---

## Índice MoSCoW

| ID | Título | Prioridade |
|----|--------|------------|
| RF-001 | Página Por Tema | Must |
| RF-002 | Página Por Plataforma | Must |
| RF-003 | Carrossel lateral sem scroll no host | Must |
| RF-004 | Quatro slides na página Por Tema | Must |
| RF-005 | Quatro slides na página Por Plataforma | Must |
| RF-006 | Embed Elasticsearch/Kibana | Must |
| RF-007 | Embed R/Shiny | Must |
| RF-008 | Homogeneidade visual entre origens | Must |
| RF-009 | Seed fictício dimensional | Must |
| RF-010 | Catálogo dos 15 temas | Must |
| RF-011 | Catálogo das 4 plataformas | Must |
| RF-012 | Análises apenas descritivas | Must |
| RF-013 | Navegação entre as duas páginas | Must |
| RF-014 | Controles e indicador do carrossel | Must |
| RF-015 | Conteúdo alinhado ao eixo da página | Should |
| RF-016 | Legendas curtas por slide | Should |
| RF-017 | Seed reprodutível | Should |
| RF-018 | Indicação de dados fictícios na UI | Could |
| RF-019 | Autenticação de embeds em produção | Won't |

---

## Catálogo

### RF-001 — Página Por Tema

- **Descrição:** O painel deve disponibilizar uma página/entrada dedicada à visualização da propagação de desinformação **por tema**.
- **Prioridade:** Must
- **Origem:** briefing REQ-001 / §5.1
- **Critério de aceite:** Dado um usuário no painel, quando acessa a entrada “Por Tema”, então visualiza exclusivamente o conteúdo dessa página (carrossel e embeds associados ao eixo tema), distinta da página Por Plataforma.
- **Destino:** SPEC-001, US-001

### RF-002 — Página Por Plataforma

- **Descrição:** O painel deve disponibilizar uma página/entrada dedicada à visualização da propagação de desinformação **por plataforma**.
- **Prioridade:** Must
- **Origem:** briefing REQ-002 / §5.1
- **Critério de aceite:** Dado um usuário no painel, quando acessa a entrada “Por Plataforma”, então visualiza exclusivamente o conteúdo dessa página, distinta da página Por Tema.
- **Destino:** SPEC-002, US-002

### RF-003 — Carrossel lateral sem scroll no host

- **Descrição:** Em cada página principal, o conteúdo além do primeiro viewport deve ser acessível por **carrossel lateral**. A página-host não deve usar scroll vertical como meio principal de navegação.
- **Prioridade:** Must
- **Origem:** briefing REQ-003 / §5.1, §7
- **Critério de aceite:** Dado o viewport alvo (desktop), quando o usuário navega o conteúdo de uma página, então não há barra de scroll vertical na página-host e a troca de conteúdo ocorre por movimento/seleção lateral do carrossel.
- **Destino:** SPEC-003, US-003

### RF-004 — Quatro slides na página Por Tema

- **Descrição:** O carrossel da página Por Tema deve conter **exatamente 4 slides**, cada um com pelo menos uma visualização gráfica.
- **Prioridade:** Must
- **Origem:** briefing REQ-001, REQ-003; decisão N=8 desta especificação
- **Critério de aceite:** Dado a página Por Tema carregada, quando se percorre o carrossel até o fim, então existem 4 posições/slides distintos e cada slide exibe ao menos um gráfico.
- **Destino:** SPEC-004, US-004

### RF-005 — Quatro slides na página Por Plataforma

- **Descrição:** O carrossel da página Por Plataforma deve conter **exatamente 4 slides**, cada um com pelo menos uma visualização gráfica.
- **Prioridade:** Must
- **Origem:** briefing REQ-002, REQ-003; decisão N=8 desta especificação
- **Critério de aceite:** Dado a página Por Plataforma carregada, quando se percorre o carrossel até o fim, então existem 4 posições/slides distintos e cada slide exibe ao menos um gráfico.
- **Destino:** SPEC-005, US-005

### RF-006 — Embed Elasticsearch/Kibana

- **Descrição:** O painel deve apresentar visualizações provenientes de Elasticsearch/Kibana embutidas na interface (isolamento tipo iframe ou equivalente funcional).
- **Prioridade:** Must
- **Origem:** briefing REQ-004 / §6
- **Critério de aceite:** Dado cada página principal (Tema e Plataforma), quando o usuário navega os slides, então ao menos um slide por página exibe visualização originada de Elasticsearch/Kibana, visível sem erro de framing.
- **Destino:** SPEC-006, US-006

### RF-007 — Embed R/Shiny

- **Descrição:** O painel deve apresentar visualizações provenientes de R/Shiny (incl. ggplot2) embutidas na interface (isolamento tipo iframe ou equivalente funcional).
- **Prioridade:** Must
- **Origem:** briefing REQ-005 / §6
- **Critério de aceite:** Dado cada página principal (Tema e Plataforma), quando o usuário navega os slides, então ao menos um slide por página exibe visualização originada de R/Shiny, visível sem erro de framing.
- **Destino:** SPEC-007, US-007

### RF-008 — Homogeneidade visual entre origens

- **Descrição:** Gráficos de origens distintas (Elasticsearch/Kibana e R/Shiny) devem ser percebidos como parte do mesmo produto: aparência visual homogênea (cores, tipografia, densidade, enquadramento).
- **Prioridade:** Must
- **Origem:** briefing REQ-006 / §5.1, §7
- **Critério de aceite:** Dado um checklist de homogeneidade (mesma paleta de tokens, mesma família tipográfica do shell, padding externo do embed alinhado), quando se comparam um embed Kibana e um embed Shiny na mesma página, então o checklist é atendido (ver RNF-005).
- **Destino:** SPEC-008, US-008

### RF-009 — Seed fictício dimensional

- **Descrição:** O ambiente de demonstração/desenvolvimento deve utilizar **seed fictício** cujas dimensões cubram as 4 plataformas, os 15 temas, as 27 UFs e os anos 2021–2024. Não deve conter dados reais de produção nem PII real.
- **Prioridade:** Must
- **Origem:** briefing REQ-007 / §5.1
- **Critério de aceite:** Dado o seed carregado, quando se inspecionam as dimensões disponíveis, então existem registros (ou agregados derivados) para cada plataforma do catálogo, cada tema do catálogo, cada UF e cada ano de 2021–2024; e não há PII real.
- **Destino:** SPEC-009, US-009

### RF-010 — Catálogo dos 15 temas

- **Descrição:** O sistema deve reconhecer e expor o catálogo fixo de **15 temas**: eleição, governo, vacinas, saúde, educação, economia, segurança, meio_ambiente, religião, gênero, imigração, ciência, mídia, justiça, outros.
- **Prioridade:** Must
- **Origem:** briefing REQ-009 (fechado nesta etapa)
- **Critério de aceite:** Dado o painel/seed, quando se listam os temas disponíveis, então a lista contém exatamente esses 15 rótulos (sem omissão nem tema fora do catálogo no eixo principal).
- **Destino:** SPEC-010, US-010

### RF-011 — Catálogo das 4 plataformas

- **Descrição:** O sistema deve reconhecer e expor o catálogo fixo de **4 plataformas**: WhatsApp, Facebook, Instagram, YouTube.
- **Prioridade:** Must
- **Origem:** briefing REQ-010 (fechado nesta etapa)
- **Critério de aceite:** Dado o painel/seed, quando se listam as plataformas disponíveis, então a lista contém exatamente essas 4 (sem omissão nem plataforma fora do catálogo no eixo principal).
- **Destino:** SPEC-011, US-011

### RF-012 — Análises apenas descritivas

- **Descrição:** As visualizações e textos do painel limitam-se a descrições e agregações simples. O produto não deve oferecer machine learning, modelos preditivos ou estatística complexa como capacidade.
- **Prioridade:** Must
- **Origem:** briefing REQ-008 / §3
- **Critério de aceite:** Dado o conjunto de slides e textos do painel, quando se revisa o escopo analítico, então não há funcionalidade de ML, previsão ou inferência estatística avançada; apenas contagens, proporções, séries/agregados descritivos e equivalentes.
- **Destino:** SPEC-012, US-012

### RF-013 — Navegação entre as duas páginas

- **Descrição:** O usuário deve poder alternar entre as páginas Por Tema e Por Plataforma por meio de navegação explícita (menu, abas ou links equivalentes).
- **Prioridade:** Must
- **Origem:** briefing REQ-001, REQ-002
- **Critério de aceite:** Dado o usuário em qualquer uma das duas páginas, quando aciona o controle de navegação para a outra, então a página correspondente é apresentada sem exigir URL digitada manualmente.
- **Destino:** SPEC-013, US-013

### RF-014 — Controles e indicador do carrossel

- **Descrição:** O carrossel deve oferecer controles para avançar e voltar e um indicador da posição atual (ex.: “2 de 4” ou equivalente perceptível).
- **Prioridade:** Must
- **Origem:** briefing REQ-003 / §7
- **Critério de aceite:** Dado um carrossel com 4 slides, quando o usuário avança e volta, então a posição muda corretamente e o indicador reflete o índice atual em todos os slides.
- **Destino:** SPEC-014, US-014

### RF-015 — Conteúdo alinhado ao eixo da página

- **Descrição:** Os slides da página Por Tema devem enfatizar o eixo **tema**; os da página Por Plataforma, o eixo **plataforma**.
- **Prioridade:** Should
- **Origem:** briefing §2, §5.1
- **Critério de aceite:** Dado cada slide, quando se lê título/legenda e o recorte do gráfico, então o eixo dominante corresponde à página em que o slide está (tema ou plataforma).
- **Destino:** SPEC-015, US-015

### RF-016 — Legendas curtas por slide

- **Descrição:** Cada slide deve apresentar texto curto de apoio compreensível ao público geral (além do gráfico).
- **Prioridade:** Should
- **Origem:** briefing REQ-008 / §3
- **Critério de aceite:** Dado cada um dos 8 slides, quando o slide está ativo, então há legenda ou texto de apoio com linguagem não especializada e sem jargão de ML/estatística avançada.
- **Destino:** SPEC-016, US-016

### RF-017 — Seed reprodutível

- **Descrição:** O seed fictício deve ser reprodutível e versionável, permitindo recriar o ambiente de demo com o mesmo domínio dimensional.
- **Prioridade:** Should
- **Origem:** briefing REQ-007; discovery RNF-010
- **Critério de aceite:** Dado o artefato de seed versionado no repositório (ou procedimento documentado), quando se aplica o procedimento de carga, então as dimensões do RF-009 ficam disponíveis novamente de forma determinística.
- **Destino:** SPEC-017, US-017

### RF-018 — Indicação de dados fictícios na UI

- **Descrição:** A interface deve indicar de forma visível que os dados apresentados são fictícios / de demonstração.
- **Prioridade:** Could
- **Origem:** briefing §4 (demo segura)
- **Critério de aceite:** Dado qualquer das duas páginas, quando a página é carregada, então há indicação persistente ou claramente visível de que os dados são fictícios.
- **Destino:** SPEC-018, US-018

### RF-019 — Autenticação de embeds em produção

- **Descrição:** Autenticação e autorização dos embeds (Kibana/Shiny) em ambiente de produção **não** fazem parte desta entrega de especificação funcional a implementar agora.
- **Prioridade:** Won't
- **Origem:** briefing §10 premissa aberta 4; discovery RK-07
- **Critério de aceite:** N/A para implementação atual. Registrado para destino futuro: a fase SPEC deve tratar política de auth pública vs restrita sem bloquear a demo local sem auth.
- **Destino:** SPEC-019, US-019

---

## Critérios de cobertura desta especificação

- [x] 2 páginas (RF-001, RF-002, RF-013)
- [x] Carrossel (RF-003, RF-014)
- [x] N=8 slides/gráficos (RF-004, RF-005)
- [x] Embeds ES+R (RF-006, RF-007)
- [x] Seed dimensional (RF-009)
- [x] 15 temas (RF-010) e 4 plataformas (RF-011)

## Próximo passo

Detalhar SPEC-001..019 e US-001..019 a partir deste catálogo e da [matriz-rastreabilidade.csv](./matriz-rastreabilidade.csv).
