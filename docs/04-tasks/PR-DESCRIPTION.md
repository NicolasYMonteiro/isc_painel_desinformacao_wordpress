# PR-001..020 — implementação DSN-DASH

## Summary
- Ambiente Docker Compose completo (`docker/`) com healthchecks e rede `dsn-net`
- Seed fictício 50k + bulk ES (`scripts/seed/`)
- Plugin WP `dsn-dashboard` (shortcode, Swiper, embeds, estados)
- Shiny + Kibana framing (ADR-001)
- CI: pytest + compose config + php -l

## Tasks
TASK-001 … TASK-020 (US-001…021). TASK-019 Won't documentado.

## Test plan
- [x] `pytest -q` (16+ tests)
- [ ] `docker compose up -d --build` (requer Docker Desktop)
- [ ] Seed + `index_to_es.py` → count 50000
- [ ] WP :8080, ES :9200, Kibana :5601, Shiny :3838/dsn/
- [ ] Ativar plugin; páginas /por-tema/ e /por-plataforma/
- [ ] `?dsn_force_error=1` e `?dsn_empty=1`
