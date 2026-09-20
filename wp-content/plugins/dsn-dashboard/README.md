# DSN Dashboard (WordPress plugin)

Plugin `dsn-dashboard` — shortcode `[dsn_dashboard page="tema"|"plataforma"]`.

## Ativação

1. Suba o stack (`docker/README.md`).
2. Em WP Admin → Plugins → ative **DSN Dashboard**.
3. Páginas ` /por-tema/` e `/por-plataforma/` são criadas na ativação.

## Variáveis de ambiente

| Var | Default |
|-----|---------|
| `DSN_KIBANA_URL` | `http://localhost:5601` |
| `DSN_SHINY_URL` | `http://localhost:3838` |

## Testes manuais

- `TEST-006` shortcode renderiza `.dsn-dashboard`
- `TEST-008` carrossel teclado + sem scroll
- `?dsn_force_error=1` → estado error (TEST-016)
- `?dsn_empty=1` → slide 4 empty na página tema (TEST-017)

## TASK-019

Auth de embeds em produção: **Won't** neste incremento.
