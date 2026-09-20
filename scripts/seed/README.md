# MOD-SEED

```bash
pip install -r requirements.txt
python scripts/seed/generate_data.py --n 50000 --seed 42
python scripts/seed/index_to_es.py --es http://localhost:9200 --recreate
python scripts/seed/validate_catalogs.py
```

Queries de exemplo:

```http
GET desinfo_events/_count

GET desinfo_events/_search
{
  "size": 0,
  "aggs": {
    "by_platform": { "terms": { "field": "platform" } },
    "by_year": { "terms": { "field": "year" } },
    "by_theme": { "terms": { "field": "theme", "size": 15 } },
    "by_uf": { "terms": { "field": "uf", "size": 27 } }
  }
}
```

RNG seed padrão: `42` (reproduzível).
