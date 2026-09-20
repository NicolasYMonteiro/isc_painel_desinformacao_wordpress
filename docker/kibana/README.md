# Saved objects Kibana (TASK-004)

Após o seed, crie um Data View no Kibana:

1. Stack Management → Data Views → Create: index pattern `desinfo_events`, time field `timestamp`
2. Dashboard → Create visualization (Lens):
   - Bar: `theme` terms + count
   - Bar: `platform` terms + sum `engagement_count`
3. Salve com IDs sugeridos para embed:
   - `dsn-by-theme`
   - `dsn-theme-engagement`
   - `dsn-by-platform`
   - `dsn-by-platform-year`

URL de embed (exemplo):

```
http://localhost:5601/app/dashboards#/view/<id>?embed=true&_g=()
```

Framing: ver `docker/kibana/kibana.yml` (`csp.frame_ancestors`, `disableEmbedding: false`).
