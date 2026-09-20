#!/usr/bin/env python3
"""
Bootstrap da demo DSN-DASH v0.1.0
Aguarda health dos serviços, gera/carrega seed, configura Kibana e WordPress.
"""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "scripts" / "seed"
NDJSON = ROOT / "data" / "generated" / "desinfo_events.ndjson"
ES = "http://localhost:9200"
WP = "http://localhost:8080"
KIBANA = "http://localhost:5601"


def wait_url(url: str, name: str, attempts: int = 90) -> None:
    for i in range(attempts):
        try:
            urllib.request.urlopen(url, timeout=5)
            print(f"OK {name}")
            return
        except Exception:
            print(f"  waiting {name} ({i + 1}/{attempts})...")
            time.sleep(3)
    raise SystemExit(f"Timeout aguardando {name}: {url}")


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd or ROOT))


def docker_wp(*args: str) -> None:
    run(["docker", "exec", "dsn-wordpress", *args])


def ensure_wp_cli() -> None:
    try:
        docker_wp("which", "wp")
    except subprocess.CalledProcessError:
        docker_wp(
            "bash",
            "-c",
            "curl -sS -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x /usr/local/bin/wp",
        )


def setup_wordpress() -> None:
    ensure_wp_cli()
    try:
        docker_wp("wp", "core", "is-installed", "--allow-root")
        print("WordPress já instalado")
    except subprocess.CalledProcessError:
        docker_wp(
            "wp",
            "core",
            "install",
            "--url=http://localhost:8080",
            "--title=DSN-DASH",
            "--admin_user=admin",
            "--admin_password=adminchangeme",
            "--admin_email=admin@example.com",
            "--skip-email",
            "--allow-root",
        )
    docker_wp("wp", "plugin", "activate", "dsn-dashboard", "--allow-root")
    docker_wp("wp", "rewrite", "structure", "/%postname%/", "--allow-root")
    docker_wp("wp", "rewrite", "flush", "--allow-root")
    print("Plugin dsn-dashboard ativo")


def main() -> None:
    print("=== DSN-DASH demo bootstrap ===")
    wait_url(ES, "Elasticsearch")
    wait_url(WP, "WordPress")
    wait_url(f"{KIBANA}/api/status", "Kibana")

    if not NDJSON.is_file():
        run([sys.executable, str(SEED_DIR / "generate_data.py"), "--n", "50000", "--seed", "42"])
    else:
        print(f"NDJSON existente: {NDJSON}")

    run(
        [
            sys.executable,
            str(SEED_DIR / "index_to_es.py"),
            "--es",
            ES,
            "--recreate",
            "--ndjson",
            str(NDJSON),
        ]
    )
    run([sys.executable, str(SEED_DIR / "validate_catalogs.py"), "--es", ES])
    run([sys.executable, str(SEED_DIR / "setup_kibana.py")])
    setup_wordpress()

    print()
    print("Demo pronta:")
    print("  http://localhost:8080/por-tema/")
    print("  http://localhost:8080/por-plataforma/")
    print("  Admin WP: http://localhost:8080/wp-admin  (admin / adminchangeme)")
    print("  Dados fictícios — demonstração")


if __name__ == "__main__":
    main()
