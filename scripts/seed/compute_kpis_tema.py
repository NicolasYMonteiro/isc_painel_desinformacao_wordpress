#!/usr/bin/env python3
"""Gera KPIs nativos dos mosaicos Tema (T1 global, T2/T3 theme, T4 geo)."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from es_http import search

DATA = Path(__file__).resolve().parents[2] / "wp-content/plugins/dsn-dashboard/data"

UF_REGION = {
    "AC": "N", "AP": "N", "AM": "N", "PA": "N", "RO": "N", "RR": "N", "TO": "N",
    "AL": "NE", "BA": "NE", "CE": "NE", "MA": "NE", "PB": "NE", "PE": "NE",
    "PI": "NE", "RN": "NE", "SE": "NE",
    "DF": "CO", "GO": "CO", "MT": "CO", "MS": "CO",
    "ES": "SE", "MG": "SE", "RJ": "SE", "SP": "SE",
    "PR": "S", "RS": "S", "SC": "S",
}


def pct_delta(cur: float, prev: float) -> float | None:
    if prev == 0:
        return None
    return round((cur - prev) / prev * 100, 1)


def write(name: str, payload: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


def kpis_theme(theme: str, label: str) -> dict:
    body = {
        "size": 0,
        "query": {"term": {"theme": theme}},
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
            "plat2023": {
                "filter": {"term": {"year": 2023}},
                "aggs": {"by": {"terms": {"field": "platform", "size": 4}}},
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
    buckets = ag["plat2024"]["by"]["buckets"]
    leader = buckets[0]["key"] if buckets else "—"
    leader_n24 = buckets[0]["doc_count"] if buckets else 0
    leader_n23 = next(
        (b["doc_count"] for b in ag["plat2023"]["by"]["buckets"] if b["key"] == leader),
        0,
    )
    return {
        "slice": {"dimension": "theme", "value": theme},
        "period": {"base": 2024, "compare": 2023},
        "generated_from": "desinfo_events",
        "kpis": [
            {
                "id": "kpi-events",
                "label": f"Eventos {label} 2024",
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
                "id": "kpi-leader",
                "label": f"Eventos {leader} 2024",
                "value": leader_n24,
                "format": "int",
                "delta_pct": pct_delta(leader_n24, leader_n23),
                "period_label": "vs 2023",
            },
        ],
    }


def kpis_global() -> dict:
    body = {
        "size": 0,
        "aggs": {
            "y2023": {
                "filter": {"term": {"year": 2023}},
                "aggs": {
                    "eng": {"sum": {"field": "engagement_count"}},
                    "by_plat": {"terms": {"field": "platform", "size": 4}},
                    "by_theme": {"terms": {"field": "theme", "size": 15}},
                },
            },
            "y2024": {
                "filter": {"term": {"year": 2024}},
                "aggs": {
                    "eng": {"sum": {"field": "engagement_count"}},
                    "by_plat": {"terms": {"field": "platform", "size": 4}},
                    "by_theme": {"terms": {"field": "theme", "size": 15}},
                },
            },
        },
    }
    ag = search(body)["aggregations"]
    ev24, ev23 = ag["y2024"]["doc_count"], ag["y2023"]["doc_count"]
    eng24 = float(ag["y2024"]["eng"]["value"] or 0)
    eng23 = float(ag["y2023"]["eng"]["value"] or 0)
    plats = ag["y2024"]["by_plat"]["buckets"]
    leader = plats[0]["key"] if plats else "—"
    leader_share24 = round(100.0 * plats[0]["doc_count"] / ev24, 1) if plats and ev24 else 0.0
    plats23 = ag["y2023"]["by_plat"]["buckets"]
    leader_share23 = 0.0
    for b in plats23:
        if b["key"] == leader and ev23:
            leader_share23 = round(100.0 * b["doc_count"] / ev23, 1)
            break
    n_themes24 = len(ag["y2024"]["by_theme"]["buckets"])
    n_themes23 = len(ag["y2023"]["by_theme"]["buckets"])
    return {
        "slice": {"dimension": "global", "value": "all"},
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
                "id": "kpi-themes",
                "label": "Temas com volume",
                "value": n_themes24,
                "format": "int",
                "delta_pct": pct_delta(n_themes24, n_themes23),
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
        ],
    }


def kpis_geo() -> dict:
    body = {
        "size": 0,
        "aggs": {
            "y2023": {
                "filter": {"term": {"year": 2023}},
                "aggs": {"by": {"terms": {"field": "uf", "size": 27}}},
            },
            "y2024": {
                "filter": {"term": {"year": 2024}},
                "aggs": {"by": {"terms": {"field": "uf", "size": 27}}},
            },
        },
    }
    ag = search(body)["aggregations"]
    ev24, ev23 = ag["y2024"]["doc_count"], ag["y2023"]["doc_count"]
    ufs = ag["y2024"]["by"]["buckets"]
    ufs23 = ag["y2023"]["by"]["buckets"]
    leader_uf = ufs[0]["key"] if ufs else "—"
    leader_n = ufs[0]["doc_count"] if ufs else 0
    uf23 = next((b["doc_count"] for b in ufs23 if b["key"] == leader_uf), 0)
    top5 = sum(b["doc_count"] for b in ufs[:5])
    conc24 = round(100.0 * top5 / ev24, 1) if ev24 else 0.0
    top5_23 = sum(b["doc_count"] for b in ufs23[:5])
    conc23 = round(100.0 * top5_23 / ev23, 1) if ev23 else 0.0
    n_ufs24 = len(ufs)
    n_ufs23 = len(ufs23)
    return {
        "slice": {"dimension": "geo", "value": "uf_region"},
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
                "id": "kpi-ufs",
                "label": "UFs com volume",
                "value": n_ufs24,
                "format": "int",
                "delta_pct": pct_delta(n_ufs24, n_ufs23),
                "period_label": "vs 2023",
            },
            {
                "id": "kpi-leader-delta",
                "label": f"Eventos {leader_uf} 2024",
                "value": leader_n,
                "format": "int",
                "delta_pct": pct_delta(leader_n, uf23),
                "period_label": "vs 2023",
            },
            {
                "id": "kpi-top5",
                "label": "Concentracao top-5 UF",
                "value": conc24,
                "format": "pct",
                "delta_pct": pct_delta(conc24, conc23),
                "period_label": "vs 2023",
            },
        ],
    }


def main() -> None:
    write("kpis-eleicao.json", kpis_theme("eleicao", "eleicao"))
    write("kpis-vacinas.json", kpis_theme("vacinas", "vacinas"))
    write("kpis-global-tema.json", kpis_global())
    write("kpis-geo.json", kpis_geo())


if __name__ == "__main__":
    main()
