# MOD-SHINY — base R apenas (build rápido; sem install.packages)
library(shiny)

seed_path <- "/data/seed/shiny_seed.csv"

load_df <- function() {
  if (!file.exists(seed_path)) {
    return(data.frame(
      platform = c("WhatsApp", "Facebook", "Instagram", "YouTube"),
      engagement_count = c(1200, 3400, 2100, 900)
    ))
  }
  raw <- read.csv(seed_path, stringsAsFactors = FALSE)
  if (!all(c("platform", "engagement_count") %in% names(raw))) {
    return(data.frame(
      platform = c("WhatsApp", "Facebook", "Instagram", "YouTube"),
      engagement_count = c(1200, 3400, 2100, 900)
    ))
  }
  aggregate(engagement_count ~ platform, data = raw, FUN = sum)
}

ui <- fluidPage(
  tags$head(tags$style(HTML("
    body { background:#0f172a; color:#e2e8f0; font-family:Segoe UI,system-ui,sans-serif; margin:0; padding:12px; }
    h3 { color:#38bdf8; margin-top:0; }
  "))),
  h3("Engajamento por plataforma (dados fictícios)"),
  plotOutput("by_platform", height = "320px")
)

server <- function(input, output, session) {
  output$by_platform <- renderPlot({
    agg <- load_df()
    op <- par(bg = "#1e293b", fg = "#e2e8f0", col.axis = "#e2e8f0", col.lab = "#e2e8f0")
    on.exit(par(op))
    barplot(
      agg$engagement_count,
      names.arg = agg$platform,
      horiz = TRUE,
      col = c("#38bdf8", "#818cf8", "#f472b6", "#fb7185"),
      border = NA,
      xlab = "Engajamento (soma)"
    )
  })
}

shinyApp(ui, server)
