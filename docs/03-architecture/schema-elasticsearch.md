# DSN-DASH — Schema Elasticsearch

| Campo | Valor |
|-------|-------|
| Índice | `desinfo_events` |
| Módulo | MOD-ES, MOD-SEED |
| Origem | RF-009..011; RNF-010 |
| Data | 2026-09-20 |

**Regra:** seed **fictício** apenas — zero PII real. Modelar **antes** da geração do seed.

---

## Propósito

Armazenar eventos fictícios de propagação de desinformação para dashboards Kibana (agregações descritivas simples). Dimensões obrigatórias: 4 plataformas × 15 temas × 27 UFs × anos 2021–2024.

---

## Campos

| Campo | Tipo ES | Obrigatório | Descrição |
|-------|---------|-------------|-----------|
| `event_id` | keyword | Sim | ID sintético único do evento |
| `timestamp` | date | Sim | Data/hora do evento (ISO-8601) |
| `year` | integer | Sim | 2021 \| 2022 \| 2023 \| 2024 |
| `platform` | keyword | Sim | WhatsApp \| Facebook \| Instagram \| YouTube |
| `theme` | keyword | Sim | Um dos 15 temas do catálogo |
| `uf` | keyword | Sim | Sigla UF (AC..TO, 27 valores) |
| `municipality_fake` | text | Não | Nome de município **fictício** (não correlacionar a pessoa) |
| `engagement_count` | long | Sim | Contagem sintética de engajamento |
| `narrative_label` | keyword | Sim | Rótulo curto de narrativa (ex.: `rumor_vacina_x`) |
| `source_channel_fake` | keyword | Sim | Canal/fonte fictícia (ex.: `canal_demo_12`) |

### Temas válidos (`theme`)

`eleicao`, `governo`, `vacinas`, `saude`, `educacao`, `economia`, `seguranca`, `meio_ambiente`, `religiao`, `genero`, `imigracao`, `ciencia`, `midia`, `justica`, `outros`

> Nota: no RF os rótulos usam acentos (`eleição`, `saúde`); no índice usamos **slugs ASCII** acima. Kibana pode mapear labels amigáveis via runtime field ou Lens.

---

## Mapping (exemplo)

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "event_id": { "type": "keyword" },
      "timestamp": { "type": "date" },
      "year": { "type": "integer" },
      "platform": { "type": "keyword" },
      "theme": { "type": "keyword" },
      "uf": { "type": "keyword" },
      "municipality_fake": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } },
      "engagement_count": { "type": "long" },
      "narrative_label": { "type": "keyword" },
      "source_channel_fake": { "type": "keyword" }
    }
  }
}
```

---

## Documento de exemplo (fictício)

```json
{
  "event_id": "evt-2023-000142",
  "timestamp": "2023-06-15T14:22:00Z",
  "year": 2023,
  "platform": "WhatsApp",
  "theme": "vacinas",
  "uf": "SP",
  "municipality_fake": "Vila Exemplo",
  "engagement_count": 1280,
  "narrative_label": "rumor_vacina_x",
  "source_channel_fake": "canal_demo_07"
}
```

---

## Agregações Kibana sugeridas (descritivas)

| Visualização candidata | Agregação |
|------------------------|-----------|
| Volume por ano | terms/histogram em `year` ou date_histogram em `timestamp` |
| Comparativo plataformas | terms em `platform` + sum `engagement_count` |
| Temas mais frequentes | terms em `theme` |
| Mapa/tabela por UF | terms em `uf` |

Sem ML, anomaly detection ou inferência complexa (RF-012).

---

## Segurança / exposição

- Índice acessível a **Kibana** via rede Docker (`API-ES`).
- **Não** publicar `9200` ao browser (RNF-009).
- Seed e bulk: MOD-SEED / `API-SEED` operacional.

## Próximo passo

Implementar gerador de seed + script de create-index/bulk alinhado a este schema.
