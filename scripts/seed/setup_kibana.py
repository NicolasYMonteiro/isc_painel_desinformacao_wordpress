"""
Cria Data View e dashboards simples via Saved Objects API (Kibana 8).
IDs: dsn-by-theme, dsn-theme-engagement, dsn-by-platform, dsn-by-platform-year
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

KIBANA = "http://localhost:5601"
H = {"Content-Type": "application/json", "kbn-xsrf": "true"}


def api(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{KIBANA}{path}", data=data, headers=H, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {err[:600]}") from e


def wait():
    for i in range(120):
        try:
            urllib.request.urlopen(f"{KIBANA}/api/status", timeout=5)
            print(f"Kibana up (attempt {i+1})")
            return
        except Exception:
            time.sleep(3)
    raise SystemExit("Kibana timeout")


def ensure_data_view():
    try:
        api(
            "POST",
            "/api/data_views/data_view",
            {
                "data_view": {
                    "id": "desinfo_events",
                    "title": "desinfo_events",
                    "name": "Desinfo Events",
                    "timeFieldName": "timestamp",
                },
                "override": True,
            },
        )
        print("OK data view desinfo_events")
    except RuntimeError as e:
        if "already" in str(e).lower() or "409" in str(e) or "exists" in str(e).lower():
            print("data view exists")
        else:
            # override path
            try:
                api("DELETE", "/api/data_views/data_view/desinfo_events")
            except Exception:
                pass
            api(
                "POST",
                "/api/data_views/data_view",
                {
                    "data_view": {
                        "id": "desinfo_events",
                        "title": "desinfo_events",
                        "name": "Desinfo Events",
                        "timeFieldName": "timestamp",
                    }
                },
            )
            print("OK data view recreated")


def vis_state_terms(field: str, metric: str = "count", metric_field: str | None = None) -> str:
    aggs = [
        {
            "id": "1",
            "enabled": True,
            "type": "count" if metric == "count" else "sum",
            "params": {} if metric == "count" else {"field": metric_field},
            "schema": "metric",
        },
        {
            "id": "2",
            "enabled": True,
            "type": "terms",
            "params": {"field": field, "orderBy": "1", "order": "desc", "size": 15},
            "schema": "segment",
        },
    ]
    state = {
        "title": field,
        "type": "horizontal_bar",
        "aggs": aggs,
        "params": {
            "type": "histogram",
            "grid": {"categoryLines": False},
            "categoryAxes": [{"id": "CategoryAxis-1", "type": "category", "position": "left", "show": True}],
            "valueAxes": [{"id": "ValueAxis-1", "type": "value", "position": "bottom", "show": True}],
            "seriesParams": [{"show": True, "type": "histogram", "mode": "stacked", "data": {"id": "1"}, "valueAxis": "ValueAxis-1"}],
            "addTooltip": True,
            "addLegend": True,
            "legendPosition": "right",
            "times": [],
            "addTimeMarker": False,
        },
    }
    return json.dumps(state)


def search_source() -> str:
    return json.dumps(
        {
            "query": {"query": "", "language": "kuery"},
            "filter": [],
            "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
        }
    )


def upsert_visualization(vid: str, title: str, field: str, metric: str = "count", metric_field: str | None = None):
    body = {
        "attributes": {
            "title": title,
            "visState": vis_state_terms(field, metric, metric_field),
            "uiStateJSON": "{}",
            "description": "DSN-DASH seed ficticio",
            "version": 1,
            "kibanaSavedObjectMeta": {"searchSourceJSON": search_source()},
        },
        "references": [
            {
                "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                "type": "index-pattern",
                "id": "desinfo_events",
            }
        ],
    }
    status, data = api("POST", f"/api/saved_objects/visualization/{vid}?overwrite=true", body)
    print("viz", vid, status)


def upsert_dashboard(did: str, title: str, viz_id: str):
    panels = [
        {
            "version": "8.15.0",
            "type": "visualization",
            "gridData": {"x": 0, "y": 0, "w": 48, "h": 20, "i": "1"},
            "panelIndex": "1",
            "embeddableConfig": {},
            "panelRefName": "panel_1",
        }
    ]
    body = {
        "attributes": {
            "title": title,
            "hits": 0,
            "description": "DSN-DASH",
            "panelsJSON": json.dumps(panels),
            "optionsJSON": json.dumps({"useMargins": True, "hidePanelTitles": False}),
            "version": 1,
            "timeRestore": False,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({"query": {"query": "", "language": "kuery"}, "filter": []})
            },
        },
        "references": [
            {"name": "panel_1", "type": "visualization", "id": viz_id},
        ],
    }
    status, _ = api("POST", f"/api/saved_objects/dashboard/{did}?overwrite=true", body)
    print("dashboard", did, status)


def ensure_index_pattern_so():
    """Saved Objects ainda referenciam index-pattern; espelha o data view."""
    body = {
        "attributes": {
            "title": "desinfo_events",
            "timeFieldName": "timestamp",
        },
    }
    try:
        api("POST", "/api/saved_objects/index-pattern/desinfo_events?overwrite=true", body)
        print("OK index-pattern SO")
    except RuntimeError as e:
        print("index-pattern warn", e)


def main():
    wait()
    ensure_data_view()
    ensure_index_pattern_so()
    upsert_visualization("viz-dsn-by-theme", "DSN By Theme", "theme")
    upsert_visualization("viz-dsn-theme-engagement", "DSN Theme Engagement", "theme", "sum", "engagement_count")
    upsert_visualization("viz-dsn-by-platform", "DSN By Platform", "platform")
    upsert_visualization("viz-dsn-by-platform-year", "DSN By Year", "year")

    upsert_dashboard("dsn-by-theme", "DSN By Theme", "viz-dsn-by-theme")
    upsert_dashboard("dsn-theme-engagement", "DSN Theme Engagement", "viz-dsn-theme-engagement")
    upsert_dashboard("dsn-by-platform", "DSN By Platform", "viz-dsn-by-platform")
    upsert_dashboard("dsn-by-platform-year", "DSN By Year", "viz-dsn-by-platform-year")

    print("\nEmbed URLs:")
    for did in ("dsn-by-theme", "dsn-theme-engagement", "dsn-by-platform", "dsn-by-platform-year"):
        print(f"http://localhost:5601/app/dashboards#/view/{did}?embed=true&_g=()")


if __name__ == "__main__":
    main()
