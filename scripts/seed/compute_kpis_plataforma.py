#!/usr/bin/env python3
"""Gera KPIs nativos dos mosaicos Por Plataforma (P1 global + P2–P4 platform)."""
from __future__ import annotations

import json
from pathlib import Path

from es_http import search

DATA = Path(__file__).resolve().parents[2] / "wp-content/plugins/dsn-dashboard/data"

# Valores exatos no seed
PLATFORMS = [
    ("WhatsApp", "whatsapp"),
    ("YouTube", "youtube"),
    ("Facebook", "facebook"),
]


def pct_delta(cur: float, prev: float) -> float | None:
    if prev == 0:
        return None
    return round((cur - prev) / prev * 100, 1)


def write(name: str, payload: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


def kpis_platform(platform: str, slug: str) -> dict:
    body = {
        "size": 0,
        "query": {"term": {"platform": platform}},
        "aggs": {
            "y2023": {
                "filter": {"term": {"year": 2023}},
                "aggs": {
                    "eng": {"sum": {"field": "engagement_count"}},
                    "by_theme": {"terms": {"field": "theme", "size": 1}},
                },
            },
            "y2024": {
                "filter": {"term": {"year": 2024}},
                "aggs": {
                    "eng": {"sum": {"field": "engagement_count"}},
                    "by_theme": {"terms": {"field": "theme", "size": 1}},
                },
            },
        },
    }
    ag = search(body)["aggregations"]
    ev24, ev23 = ag["y2024"]["doc_count"], ag["y2023"]["doc_count"]
    eng24 = float(ag["y2024"]["eng"]["value"] or 0)
    eng23 = float(ag["y2023"]["eng"]["value"] or 0)
    total24 = search(
        {"size": 0, "query": {"term": {"year": 2024}}, "track_total_hits": True}
    )["hits"]["total"]["value"]
    total23 = search(
        {"size": 0, "query": {"term": {"year": 2023}}, "track_total_hits": True}
    )["hits"]["total"]["value"]
    share24 = round(100.0 * ev24 / total24, 1) if total24 else 0.0
    share23 = round(100.0 * ev23 / total23, 1) if total23 else 0.0
    themes = ag["y2024"]["by_theme"]["buckets"]
    top_theme = themes[0]["key"] if themes else "—"
    top_n24 = themes[0]["doc_count"] if themes else 0
    top_n23 = next(
        (b["doc_count"] for b in ag["y2023"]["by_theme"]["buckets"] if b["key"] == top_theme),
        0,
    )
    return {
        "slice": {"dimension": "platform", "value": platform},
        "period": {"base": 2024, "compare": 2023},
        "generated_from": "desinfo_events",
        "kpis": [
            {
                "id": "kpi-events",
                "label": f"Eventos {platform} 2024",
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
                "value": share24,
                "format": "pct",
                "delta_pct": pct_delta(share24, share23),
                "period_label": "vs 2023",
            },
            {
                "id": "kpi-theme",
                "label": f"Eventos {top_theme} 2024",
                "value": top_n24,
                "format": "int",
                "delta_pct": pct_delta(top_n24, top_n23),
                "period_label": "vs 2023",
            },
        ],
    }


def kpis_global_plat() -> dict:
    body = {
        "size": 0,
        "aggs": {
            "y2023": {
                "filter": {"term": {"year": 2023}},
                "aggs": {
                    "eng": {"sum": {"field": "engagement_count"}},
                    "by": {"terms": {"field": "platform", "size": 4}},
                },
            },
            "y2024": {
                "filter": {"term": {"year": 2024}},
                "aggs": {
                    "eng": {"sum": {"field": "engagement_count"}},
                    "by": {"terms": {"field": "platform", "size": 4}},
                },
            },
        },
    }
    ag = search(body)["aggregations"]
    ev24, ev23 = ag["y2024"]["doc_count"], ag["y2023"]["doc_count"]
    eng24 = float(ag["y2024"]["eng"]["value"] or 0)
    eng23 = float(ag["y2023"]["eng"]["value"] or 0)
    plats = ag["y2024"]["by"]["buckets"]
    plats23 = ag["y2023"]["by"]["buckets"]
    leader = plats[0]["key"] if plats else "—"
    leader_share24 = round(100.0 * plats[0]["doc_count"] / ev24, 1) if plats and ev24 else 0.0
    leader_share23 = 0.0
    for b in plats23:
        if b["key"] == leader and ev23:
            leader_share23 = round(100.0 * b["doc_count"] / ev23, 1)
            break
    n_plats24 = len(plats)
    n_plats23 = len(plats23)
    return {
        "slice": {"dimension": "global", "value": "platform_angle"},
        "period": {"base": 2024, "compare": 2023},
        "generated_from": "desinfo_events",
        "kpis": [
            {
                "id": "kpi-events",
                "label": "Eventos 2024",
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
                "id": "kpi-leader",
                "label": f"Lider {leader}",
                "value": leader_share24,
                "format": "pct",
                "delta_pct": pct_delta(leader_share24, leader_share23),
                "period_label": "vs 2023",
            },
            {
                "id": "kpi-plats",
                "label": "Plataformas ativas",
                "value": n_plats24,
                "format": "int",
                "delta_pct": pct_delta(n_plats24, n_plats23),
                "period_label": "vs 2023",
            },
        ],
    }


def main() -> None:
    write("kpis-global-plataforma.json", kpis_global_plat())
    for platform, slug in PLATFORMS:
        write(f"kpis-{slug}.json", kpis_platform(platform, slug))


if __name__ == "__main__":
    main()
