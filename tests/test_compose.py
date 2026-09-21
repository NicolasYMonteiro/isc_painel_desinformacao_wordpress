"""TEST-001 — validação estrutural do docker-compose."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

COMPOSE = Path(__file__).resolve().parents[1] / "docker" / "docker-compose.yml"


def test_compose_file_exists():
    assert COMPOSE.is_file()


def test_compose_required_services():
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    services = set(data["services"].keys())
    assert {"wordpress", "db", "elasticsearch", "kibana", "shiny"}.issubset(services)


def test_compose_ports():
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    wp_ports = data["services"]["wordpress"].get("ports", [])
    es_ports = data["services"]["elasticsearch"].get("ports", [])
    kb_ports = data["services"]["kibana"].get("ports", [])
    shiny_ports = data["services"]["shiny"].get("ports", [])
    assert any("8080" in str(p) for p in wp_ports)
    # BUG-004 / RNF-009: ES não deve publicar 9200 no host
    assert not any("9200" in str(p) for p in es_ports)
    assert any("5601" in str(p) for p in kb_ports)
    assert any("3838" in str(p) for p in shiny_ports)


def test_compose_network_dsn_net():
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    assert "dsn-net" in data.get("networks", {})


def test_compose_healthchecks():
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    for name in ("wordpress", "db", "elasticsearch", "kibana", "shiny"):
        assert "healthcheck" in data["services"][name], f"missing healthcheck: {name}"


def test_es_security_disabled():
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    env = data["services"]["elasticsearch"].get("environment", [])
    flat = " ".join(str(x) for x in env) if isinstance(env, list) else " ".join(
        f"{k}={v}" for k, v in env.items()
    )
    assert "xpack.security.enabled=false" in flat.replace(" ", "")


def test_plugin_volume_mounted():
    data = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    vols = data["services"]["wordpress"].get("volumes", [])
    assert any("dsn-dashboard" in str(v) for v in vols)
