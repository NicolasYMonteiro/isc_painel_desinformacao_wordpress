# Saved objects Kibana (TASK-004)

## Automático (recomendado)

Com ES indexado e Kibana no ar:

```bash
py -3 scripts/seed/setup_kibana.py
```

Cria Data View `desinfo_events` + dashboards:

| ID | Conteúdo |
|----|----------|
| `dsn-by-theme` | contagem por tema |
| `dsn-theme-engagement` | soma engagement por tema |
| `dsn-by-platform` | contagem por plataforma |
| `dsn-by-platform-year` | contagem por ano |

## Embed URLs

Incluem janela temporal do seed (2021–2025) e `embed=true`:

```
http://localhost:5601/app/dashboards#/view/dsn-by-theme?embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'2021-01-01T00:00:00.000Z',to:'2025-01-01T00:00:00.000Z'))&hide-filter-bar=true
```

(os demais IDs seguem o mesmo padrão)

Visualizações: **Vega-Lite** (não aggs legadas) — evita TypeError/`mode` no Kibana 8.15.

Framing: `docker/kibana/kibana.yml` (`csp.frame_ancestors`, `disableEmbedding: false`).
