# Manual de demonstração — DSN-DASH v0.1.0

Público: clientes / stakeholders. Duração sugerida: **8–12 minutos**.

## Antes de começar

Concluir os 5 passos do [README](../../README.md). Confirmar:

- Badge **“Dados fictícios — demonstração”** visível
- Páginas `/por-tema/` e `/por-plataforma/` carregam

## Roteiro

### 1. Contexto (1 min)

> “Este é o DSN-DASH: um painel para explorar a **propagação de desinformação** de forma simples — só contagens e agregações, sem machine learning. Os dados desta demo são **100% fictícios**.”

Apontar o badge no canto superior.

### 2. Página Por Tema (3–4 min)

1. Abrir http://localhost:8080/por-tema/
2. Explicar o carrossel: **4 slides**, navegação lateral (setas / teclado), indicador “n / 4”
3. Percorrer os slides:
   - Slides **Kibana**: barras por tema/engajamento (dados do Elasticsearch)
   - Slides **Shiny**: gráfico complementar — reforçar homogeneidade visual
4. Destacar legendas curtas em linguagem acessível

### 3. Página Por Plataforma (3–4 min)

1. Clicar em **Por Plataforma** na navegação do painel
2. Repetir o carrossel no eixo plataformas (WhatsApp, Facebook, Instagram, YouTube no domínio do seed)
3. Reforçar: mesmas regras de UX (sem depender de scroll como navegação principal do conteúdo do carrossel)

### 4. Fechamento (1–2 min)

> “Próximos passos do produto: dados reais, endurecimento de segurança (ES não público), scroll do host e mais fontes.”

Não prometer prazos. Encaminhar dúvidas ao time técnico.

## O que não mostrar / como tratar

| Situação | Como falar |
|----------|------------|
| Banner “Your data is not secure” no Kibana | “Aviso padrão do stack sem security na demo local; pode dispensar.” |
| Barra de scroll do tema WP | “Resíduo do tema WordPress; o carrossel do produto é o eixo de navegação.” |
| Pedido de dados reais | “Fora do escopo desta demo; seed sintético deliberado.” |

## Checklist pós-demo

- [ ] Cliente viu as **duas** páginas
- [ ] Entendeu que dados são fictícios
- [ ] Recebeu link das [release notes](./release-notes.md)
