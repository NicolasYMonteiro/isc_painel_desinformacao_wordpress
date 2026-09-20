"""TEST-006 — contrato do shortcode presente no plugin."""
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1] / "wp-content" / "plugins" / "dsn-dashboard"


def test_plugin_files_exist():
    assert (PLUGIN / "dsn-dashboard.php").is_file()
    assert (PLUGIN / "includes" / "class-dsn-shortcode.php").is_file()
    assert (PLUGIN / "assets" / "js" / "dsn-dashboard.js").is_file()
    assert (PLUGIN / "assets" / "css" / "dsn-dashboard.css").is_file()


def test_shortcode_contract_in_source():
    src = (PLUGIN / "includes" / "class-dsn-shortcode.php").read_text(encoding="utf-8")
    assert "dsn_dashboard" in src
    assert 'page' in src
    assert "dsn-embed-frame" in src
    assert "data-state" in src
    assert "kibana" in src and "shiny" in src
