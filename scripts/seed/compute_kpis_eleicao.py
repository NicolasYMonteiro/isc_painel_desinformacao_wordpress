#!/usr/bin/env python3
"""Gera KPIs nativos do mosaico Eleição (theme=eleicao) a partir do ES."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ES = "http://localhost:9200"
OUT = Path(__file__).resolve().parents[2] / "wp-content/plugins/dsn-dashboard/data/kpis-eleicao.json"


def search(body: dict) -> dict:
    req = urllib.request.Request(
        f"{ES}/desinfo_events/_search",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def pct_delta(cur: float, prev: float) -> float | None:
    if prev == 0:
        return None
    return round((cur - prev) / prev * 100, 1)


def main() -> None:
    body = {
        "size": 0,
        "query": {"term": {"theme": "eleicao"}},
        "aggs": {
            "y2023": {
                "filter": {"term": {"year": 2023}},
                "aggs": {"eng": {"sum": {"field": "engagement_count"}}},
            },
            "y2024": {
                "filter": {"term": {"year": 2024}},
                "aggs": {"eng": {"sum": {"field": "engagement_count"}}},
            },
            "plat2024": {
                "filter": {"term": {"year": 2024}},
                "aggs": {"by": {"terms": {"field": "platform", "size": 4}}},
            },
        },
    }
    data = search(body)
    ag = data["aggregations"]
    ev24 = ag["y2024"]["doc_count"]
    ev23 = ag["y2023"]["doc_count"]
    eng24 = float(ag["y2024"]["eng"]["value"] or 0)
    eng23 = float(ag["y2023"]["eng"]["value"] or 0)

    total24 = search(
        {"size": 0, "query": {"term": {"year": 2024}}, "track_total_hits": True}
    )["hits"]["total"]["value"]
    share = round(100.0 * ev24 / total24, 1) if total24 else 0.0

    buckets = ag["plat2024"]["by"]["buckets"]
    leader = buckets[0]["key"] if buckets else "—"

    payload = {
        "slice": {"dimension": "theme", "value": "eleicao"},
        "period": {"base": 2024, "compare": 2023},
        "generated_from": "desinfo_events",
        "kpis": [
            {
                "id": "kpi-events",
                "label": "Eventos eleição 2024",
                "value": ev24,
                "format": "int",
                "delta_pct": pct_delta(ev24, ev23),
                "period_label": "vs 2023",
            },
            {
                "id": "kpi-engagement",
                "label": "Engajamento soma 2024",
                "value": int(eng24),
                "format": "int",
                "delta_pct": pct_delta(eng24, eng23),
                "period_label": "vs 2023",
            },
            {
                "id": "kpi-share",
                "label": "Share no total 2024",
                "value": share,
                "format": "pct",
                "delta_pct": None,
                "period_label": "do volume nacional",
            },
            {
                "id": "kpi-leader",
                "label": "Plataforma líder",
                "value": leader,
                "format": "text",
                "delta_pct": None,
                "period_label": "em 2024",
            },
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(payload["kpis"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
