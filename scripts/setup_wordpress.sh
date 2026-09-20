#!/usr/bin/env bash
# Instala WP (se necessário) e ativa o plugin dsn-dashboard
set -euo pipefail
WP="docker exec dsn-wordpress"

echo "Waiting WordPress..."
for i in $(seq 1 60); do
  if $WP bash -c "curl -fsS http://127.0.0.1 >/dev/null 2>&1 || php -r 'exit(0);'"; then
    break
  fi
  sleep 3
done

# Instala WP-CLI no container se necessário
if ! $WP which wp >/dev/null 2>&1; then
  $WP bash -c 'curl -sS -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x /usr/local/bin/wp'
fi

if ! $WP wp core is-installed --allow-root 2>/dev/null; then
  echo "Installing WordPress..."
  $WP wp core install \
    --url="http://localhost:8080" \
    --title="DSN-DASH" \
    --admin_user="admin" \
    --admin_password="adminchangeme" \
    --admin_email="admin@example.com" \
    --skip-email \
    --allow-root
fi

$WP wp plugin activate dsn-dashboard --allow-root
$WP wp rewrite structure '/%postname%/' --allow-root
$WP wp rewrite flush --allow-root

echo "Plugin ativo. Páginas:"
$WP wp post list --post_type=page --fields=ID,post_title,post_name,post_status --allow-root
echo "Login: http://localhost:8080/wp-admin  user=admin pass=adminchangeme"
