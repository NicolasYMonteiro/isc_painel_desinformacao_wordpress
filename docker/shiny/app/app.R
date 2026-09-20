# MOD-SHINY — visualização descritiva (TASK-005 / US-007)
library(shiny)
library(ggplot2)
library(dplyr)
library(readr)

seed_path <- "/data/seed/shiny_seed.csv"
fallback <- data.frame(
  year = c(2021L, 2022L, 2022L, 2023L),
  platform = c("WhatsApp", "Facebook", "Instagram", "YouTube"),
  theme = c("vacinas", "eleicao", "eleicao", "governo"),
  uf = c("SP", "RJ", "MG", "BA"),
  engagement_count = c(1200L, 3400L, 2100L, 900L)
)

df <- if (file.exists(seed_path)) {
  read_csv(seed_path, show_col_types = FALSE)
} else {
  fallback
}

ui <- fluidPage(
  tags$head(tags$style(HTML("
    :root {
      --dsn-color-bg: #0f172a;
      --dsn-color-surface: #1e293b;
      --dsn-color-accent: #38bdf8;
      --dsn-color-text: #e2e8f0;
      --dsn-font-family: 'Segoe UI', system-ui, sans-serif;
    }
    body { background: var(--dsn-color-bg); color: var(--dsn-color-text);
           font-family: var(--dsn-font-family); margin: 0; padding: 12px; }
    h3 { color: var(--dsn-color-accent); margin-top: 0; }
    .shiny-plot-output { background: var(--dsn-color-surface); border-radius: 8px; }
  "))),
  h3("Engajamento por plataforma (dados fictícios)"),
  plotOutput("by_platform", height = "320px")
)

server <- function(input, output, session) {
  output$by_platform <- renderPlot({
    agg <- df %>%
      group_by(platform) %>%
      summarise(total = sum(engagement_count, na.rm = TRUE), .groups = "drop")
    ggplot(agg, aes(x = reorder(platform, total), y = total, fill = platform)) +
      geom_col(show.legend = FALSE) +
      coord_flip() +
      scale_fill_manual(values = c(
        WhatsApp = "#38bdf8", Facebook = "#818cf8",
        Instagram = "#f472b6", YouTube = "#fb7185"
      )) +
      labs(x = NULL, y = "Engajamento (soma)", title = NULL) +
      theme_minimal(base_family = "sans") +
      theme(
        plot.background = element_rect(fill = "#1e293b", color = NA),
        panel.background = element_rect(fill = "#1e293b", color = NA),
        text = element_text(color = "#e2e8f0"),
        axis.text = element_text(color = "#e2e8f0"),
        panel.grid.major = element_line(color = "#334155"),
        panel.grid.minor = element_blank()
      )
  })
}

shinyApp(ui, server)
