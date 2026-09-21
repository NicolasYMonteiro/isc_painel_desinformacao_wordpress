"""
Cria Data View e dashboards Vega (Kibana 8) embedáveis.
IDs: dsn-by-theme, dsn-theme-engagement, dsn-by-platform, dsn-by-platform-year

Usa Vega em vez de visualizations aggs legadas — estas quebram no 8.15
(TypeError reading 'mode') e deixam o iframe em loading eterno.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

KIBANA = "http://localhost:5601"
H = {"Content-Type": "application/json", "kbn-xsrf": "true"}

# Tokens alinhados ao host (--dsn-*) — RNF-005
VEGA_BG = "#1e293b"
VEGA_FG = "#e2e8f0"
VEGA_ACCENT = "#38bdf8"

# Janela alinhada ao seed 2021–2024 (Rison para _g na URL de embed)
EMBED_G = (
    "(filters:!(),refreshInterval:(pause:!t,value:0),"
    "time:(from:'2021-01-01T00:00:00.000Z',to:'2025-01-01T00:00:00.000Z'))"
)


def _vega_config() -> dict:
    return {
        "view": {"stroke": None},
        "background": VEGA_BG,
        "axis": {
            "labelFontSize": 11,
            "titleFontSize": 12,
            "labelColor": VEGA_FG,
            "titleColor": VEGA_FG,
            "domainColor": "#334155",
            "tickColor": "#334155",
            "gridColor": "#334155",
        },
        "title": {"color": VEGA_FG, "fontSize": 13},
        "legend": {"labelColor": VEGA_FG, "titleColor": VEGA_FG},
    }


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
        if "409" in str(e) or "exists" in str(e).lower() or "already" in str(e).lower():
            print("data view exists")
        else:
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


def ensure_index_pattern_so():
    body = {
        "attributes": {
            "title": "desinfo_events",
            "timeFieldName": "timestamp",
        },
    }
    api("POST", "/api/saved_objects/index-pattern/desinfo_events?overwrite=true", body)
    print("OK index-pattern SO")


def _time_filters(*extra):
    filters = [
        {
            "range": {
                "timestamp": {
                    "gte": "2021-01-01T00:00:00.000Z",
                    "lte": "2025-01-01T00:00:00.000Z",
                }
            }
        }
    ]
    filters.extend(extra)
    return {"bool": {"filter": filters}}


def vega_terms_spec(
    field: str,
    title: str,
    metric: str = "count",
    theme_filter: str | None = None,
    platform_filter: str | None = None,
    width: int = 720,
    height: int = 360,
    size: int = 15,
) -> str:
    """Vega-Lite horizontal bar against ES terms agg."""
    if metric == "sum":
        aggs = {
            "cats": {
                "terms": {"field": field, "size": size, "order": {"eng": "desc"}},
                "aggs": {"eng": {"sum": {"field": "engagement_count"}}},
            }
        }
        x_field = "eng.value"
        x_title = "Engajamento (soma)"
    else:
        aggs = {"cats": {"terms": {"field": field, "size": size}}}
        x_field = "doc_count"
        x_title = "Eventos"

    body: dict = {"size": 0, "aggs": aggs}
    use_context = theme_filter is None and platform_filter is None
    extras = []
    if theme_filter:
        extras.append({"term": {"theme": theme_filter}})
    if platform_filter:
        extras.append({"term": {"platform": platform_filter}})
    if extras:
        body["query"] = _time_filters(*extras)

    url: dict = {"index": "desinfo_events", "body": body}
    if use_context:
        url["%context%"] = True
        url["%timefield%"] = "timestamp"

    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": title,
        "data": {
            "url": url,
            "format": {"property": "aggregations.cats.buckets"},
        },
        "autosize": "none",
        "width": width,
        "height": height,
        "mark": {"type": "bar", "tooltip": True, "cornerRadiusEnd": 2},
        "encoding": {
            "y": {
                "field": "key",
                "type": "nominal",
                "sort": "-x",
                "axis": {"title": None, "labelLimit": 160},
            },
            "x": {
                "field": x_field,
                "type": "quantitative",
                "axis": {"title": x_title},
            },
            "color": {"value": VEGA_ACCENT},
        },
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 13},
            "background": VEGA_BG,
        },
    }
    return json.dumps(spec)


def vega_line_monthly_spec(
    title: str,
    theme_filter: str | None = None,
    platform_filter: str | None = None,
    width: int = 900,
    height: int = 200,
) -> str:
    extras = []
    if theme_filter:
        extras.append({"term": {"theme": theme_filter}})
    if platform_filter:
        extras.append({"term": {"platform": platform_filter}})
    body = {
        "size": 0,
        "query": _time_filters(*extras),
        "aggs": {
            "months": {
                "date_histogram": {
                    "field": "timestamp",
                    "calendar_interval": "month",
                    "min_doc_count": 0,
                }
            }
        },
    }
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": title,
        "data": {
            "url": {"index": "desinfo_events", "body": body},
            "format": {"property": "aggregations.months.buckets"},
        },
        "autosize": "none",
        "width": width,
        "height": height,
        "mark": {"type": "line", "point": True, "tooltip": True, "color": VEGA_ACCENT},
        "encoding": {
            "x": {
                "field": "key_as_string",
                "type": "temporal",
                "axis": {"title": None, "format": "%b/%y"},
            },
            "y": {
                "field": "doc_count",
                "type": "quantitative",
                "axis": {"title": "Eventos / mes"},
            },
        },
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 11, "titleFontSize": 12},
            "background": VEGA_BG,
        },
    }
    return json.dumps(spec)


def vega_heatmap_theme_year_spec(title: str, platform_filter: str, width: int = 280, height: int = 200) -> str:
    body = {
        "size": 0,
        "query": _time_filters({"term": {"platform": platform_filter}}),
        "aggs": {
            "themes": {
                "terms": {"field": "theme", "size": 8},
                "aggs": {"years": {"terms": {"field": "year", "size": 4}}},
            }
        },
    }
    # Flatten nested buckets into rows via Vega transform
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": title,
        "data": {
            "url": {"index": "desinfo_events", "body": body},
            "format": {"property": "aggregations.themes.buckets"},
        },
        "transform": [
            {"flatten": ["years.buckets"]},
            {"calculate": "datum['years.buckets'].key", "as": "year"},
            {"calculate": "datum['years.buckets'].doc_count", "as": "count"},
        ],
        "autosize": "none",
        "width": width,
        "height": height,
        "mark": {"type": "rect", "tooltip": True},
        "encoding": {
            "x": {"field": "year", "type": "ordinal", "title": "Ano"},
            "y": {"field": "key", "type": "nominal", "title": None},
            "color": {
                "field": "count",
                "type": "quantitative",
                "scale": {"scheme": "blues"},
                "legend": {"title": "N"},
            },
        },
        "config": {"view": {"stroke": None}, "background": VEGA_BG},
    }
    return json.dumps(spec)


def upsert_vega_visualization(
    vid: str,
    title: str,
    field: str | None = None,
    metric: str = "count",
    *,
    theme_filter: str | None = None,
    platform_filter: str | None = None,
    line_monthly: bool = False,
    width: int = 720,
    height: int = 360,
    size: int = 15,
):
    if line_monthly:
        spec = vega_line_monthly_spec(
            title,
            theme_filter=theme_filter,
            platform_filter=platform_filter,
            width=width,
            height=height,
        )
    else:
        assert field is not None
        spec = vega_terms_spec(
            field,
            title,
            metric,
            theme_filter=theme_filter,
            platform_filter=platform_filter,
            width=width,
            height=height,
            size=size,
        )
    vis_state = {
        "title": title,
        "type": "vega",
        "params": {"spec": spec},
        "aggs": [],
    }
    body = {
        "attributes": {
            "title": title,
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "DSN-DASH seed ficticio (Vega)",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps(
                    {
                        "query": {"query": "", "language": "kuery"},
                        "filter": [],
                    }
                )
            },
        },
        "references": [],
    }
    status, _ = api("POST", f"/api/saved_objects/visualization/{vid}?overwrite=true", body)
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
            "timeRestore": True,
            "timeFrom": "2021-01-01T00:00:00.000Z",
            "timeTo": "2025-01-01T00:00:00.000Z",
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps(
                    {"query": {"query": "", "language": "kuery"}, "filter": []}
                )
            },
        },
        "references": [
            {"name": "panel_1", "type": "visualization", "id": viz_id},
        ],
    }
    status, _ = api("POST", f"/api/saved_objects/dashboard/{did}?overwrite=true", body)
    print("dashboard", did, status)



def upsert_multi_panel_dashboard(did: str, title: str, panels_spec: list[dict]):
    """RNF-003: um dashboard com N painéis (1 iframe no host).

    panels_spec: [{viz_id, x, y, w, h}, ...]
    """
    panels = []
    refs = []
    for i, pspec in enumerate(panels_spec, start=1):
        pid = str(i)
        panels.append(
            {
                "version": "8.15.0",
                "type": "visualization",
                "gridData": {
                    "x": pspec["x"],
                    "y": pspec["y"],
                    "w": pspec["w"],
                    "h": pspec["h"],
                    "i": pid,
                },
                "panelIndex": pid,
                "embeddableConfig": {},
                "panelRefName": f"panel_{pid}",
            }
        )
        refs.append(
            {"name": f"panel_{pid}", "type": "visualization", "id": pspec["viz_id"]}
        )
    body = {
        "attributes": {
            "title": title,
            "hits": 0,
            "description": "DSN-DASH mosaico multi-painel",
            "panelsJSON": json.dumps(panels),
            "optionsJSON": json.dumps({"useMargins": True, "hidePanelTitles": False}),
            "version": 1,
            "timeRestore": True,
            "timeFrom": "2021-01-01T00:00:00.000Z",
            "timeTo": "2025-01-01T00:00:00.000Z",
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps(
                    {"query": {"query": "", "language": "kuery"}, "filter": []}
                )
            },
        },
        "references": refs,
    }
    status, _ = api("POST", f"/api/saved_objects/dashboard/{did}?overwrite=true", body)
    print("dashboard", did, status, f"({len(panels)} panels)")


def upsert_mosaic_theme_pattern_a(theme: str, title_pt: str, slug: str):
    """Padrão A — linha + barras plataforma + barras UF filtrados ao tema."""
    upsert_vega_visualization(
        f"viz-mosaic-{slug}-line",
        f"{title_pt} — serie mensal",
        line_monthly=True,
        theme_filter=theme,
        width=880,
        height=180,
    )
    upsert_vega_visualization(
        f"viz-mosaic-{slug}-platform",
        f"{title_pt} — por plataforma",
        "platform",
        theme_filter=theme,
        width=420,
        height=220,
        size=4,
    )
    upsert_vega_visualization(
        f"viz-mosaic-{slug}-uf",
        f"{title_pt} — top UF",
        "uf",
        theme_filter=theme,
        width=420,
        height=220,
        size=10,
    )
    upsert_multi_panel_dashboard(
        f"dsn-mosaic-{slug}",
        f"DSN Mosaic {title_pt}",
        [
            {"viz_id": f"viz-mosaic-{slug}-line", "x": 0, "y": 0, "w": 48, "h": 12},
            {"viz_id": f"viz-mosaic-{slug}-platform", "x": 0, "y": 12, "w": 24, "h": 12},
            {"viz_id": f"viz-mosaic-{slug}-uf", "x": 24, "y": 12, "w": 24, "h": 12},
        ],
    )


def vega_donut_platform_spec(title: str, width: int = 320, height: int = 220) -> str:
    body = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "timestamp": {
                                "gte": "2021-01-01T00:00:00.000Z",
                                "lte": "2025-01-01T00:00:00.000Z",
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {"cats": {"terms": {"field": "platform", "size": 4}}},
    }
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": title,
        "data": {
            "url": {"index": "desinfo_events", "body": body},
            "format": {"property": "aggregations.cats.buckets"},
        },
        "autosize": "none",
        "width": width,
        "height": height,
        "mark": {"type": "arc", "tooltip": True, "innerRadius": 50},
        "encoding": {
            "theta": {"field": "doc_count", "type": "quantitative"},
            "color": {"field": "key", "type": "nominal", "legend": {"title": "Plataforma"}},
        },
        "config": {"background": VEGA_BG, "view": {"stroke": None}},
    }
    return json.dumps(spec)


def vega_line_global_spec(title: str, width: int = 420, height: int = 200) -> str:
    body = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "timestamp": {
                                "gte": "2021-01-01T00:00:00.000Z",
                                "lte": "2025-01-01T00:00:00.000Z",
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "months": {
                "date_histogram": {
                    "field": "timestamp",
                    "calendar_interval": "month",
                    "min_doc_count": 0,
                }
            }
        },
    }
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": title,
        "data": {
            "url": {"index": "desinfo_events", "body": body},
            "format": {"property": "aggregations.months.buckets"},
        },
        "autosize": "none",
        "width": width,
        "height": height,
        "mark": {"type": "line", "point": True, "tooltip": True, "color": VEGA_ACCENT},
        "encoding": {
            "x": {
                "field": "key_as_string",
                "type": "temporal",
                "axis": {"title": None, "format": "%b/%y"},
            },
            "y": {
                "field": "doc_count",
                "type": "quantitative",
                "axis": {"title": "Eventos / mes"},
            },
        },
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 11, "titleFontSize": 12},
            "background": VEGA_BG,
        },
    }
    return json.dumps(spec)


def vega_region_bars_spec(title: str, width: int = 420, height: int = 220) -> str:
    """Barras por macrorregiao via script terms (fallback do mapa)."""
    script = """
String uf = doc.containsKey('uf') && doc['uf'].size()!=0 ? doc['uf'].value : '';
if (['AC','AP','AM','PA','RO','RR','TO'].contains(uf)) return 'N';
if (['AL','BA','CE','MA','PB','PE','PI','RN','SE'].contains(uf)) return 'NE';
if (['DF','GO','MT','MS'].contains(uf)) return 'CO';
if (['ES','MG','RJ','SP'].contains(uf)) return 'SE';
if (['PR','RS','SC'].contains(uf)) return 'S';
return 'OUTRO';
"""
    body = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "timestamp": {
                                "gte": "2021-01-01T00:00:00.000Z",
                                "lte": "2025-01-01T00:00:00.000Z",
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "cats": {
                "terms": {
                    "script": {"source": script, "lang": "painless"},
                    "size": 6,
                }
            }
        },
    }
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": title,
        "data": {
            "url": {"index": "desinfo_events", "body": body},
            "format": {"property": "aggregations.cats.buckets"},
        },
        "autosize": "none",
        "width": width,
        "height": height,
        "mark": {"type": "bar", "tooltip": True, "cornerRadiusEnd": 2},
        "encoding": {
            "y": {"field": "key", "type": "nominal", "sort": "-x", "axis": {"title": None}},
            "x": {"field": "doc_count", "type": "quantitative", "axis": {"title": "Eventos"}},
            "color": {"value": VEGA_ACCENT},
        },
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 13},
            "background": VEGA_BG,
        },
    }
    return json.dumps(spec)


def upsert_vega_raw(vid: str, title: str, spec_json: str):
    vis_state = {"title": title, "type": "vega", "params": {"spec": spec_json}, "aggs": []}
    body = {
        "attributes": {
            "title": title,
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "DSN-DASH mosaico",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps(
                    {"query": {"query": "", "language": "kuery"}, "filter": []}
                )
            },
        },
        "references": [],
    }
    status, _ = api("POST", f"/api/saved_objects/visualization/{vid}?overwrite=true", body)
    print("viz", vid, status)


def upsert_mosaic_pattern_c():
    """T1 — barras por tema + linha global + donut plataforma."""
    upsert_vega_visualization(
        "viz-mosaic-t1-themes",
        "Volume por tema",
        "theme",
        width=880,
        height=200,
        size=15,
    )
    upsert_vega_raw(
        "viz-mosaic-t1-line",
        "Evolucao total mensal",
        vega_line_global_spec("Evolucao total mensal", width=400, height=200),
    )
    upsert_vega_raw(
        "viz-mosaic-t1-donut",
        "Share por plataforma",
        vega_donut_platform_spec("Share por plataforma"),
    )
    upsert_multi_panel_dashboard(
        "dsn-mosaic-t1",
        "DSN Mosaic T1",
        [
            {"viz_id": "viz-mosaic-t1-themes", "x": 0, "y": 0, "w": 48, "h": 12},
            {"viz_id": "viz-mosaic-t1-line", "x": 0, "y": 12, "w": 24, "h": 12},
            {"viz_id": "viz-mosaic-t1-donut", "x": 24, "y": 12, "w": 24, "h": 12},
        ],
    )


def upsert_mosaic_pattern_d():
    """T4 — regioes + top UF + linha nacional."""
    upsert_vega_raw(
        "viz-mosaic-t4-regions",
        "Eventos por macrorregiao",
        vega_region_bars_spec("Eventos por macrorregiao"),
    )
    upsert_vega_visualization(
        "viz-mosaic-t4-uf",
        "Top 10 UF",
        "uf",
        width=420,
        height=220,
        size=10,
    )
    upsert_vega_raw(
        "viz-mosaic-t4-line",
        "Serie mensal nacional",
        vega_line_global_spec("Serie mensal nacional", width=880, height=180),
    )
    upsert_multi_panel_dashboard(
        "dsn-mosaic-t4",
        "DSN Mosaic T4",
        [
            {"viz_id": "viz-mosaic-t4-regions", "x": 0, "y": 0, "w": 24, "h": 12},
            {"viz_id": "viz-mosaic-t4-uf", "x": 24, "y": 0, "w": 24, "h": 12},
            {"viz_id": "viz-mosaic-t4-line", "x": 0, "y": 12, "w": 48, "h": 12},
        ],
    )


def upsert_mosaic_platform_pattern_b(platform: str, title_pt: str, slug: str):
    """Padrão B — linha + heatmap tema×ano + barras temas."""
    upsert_vega_visualization(
        f"viz-mosaic-{slug}-line",
        f"{title_pt} — serie mensal",
        line_monthly=True,
        platform_filter=platform,
        width=560,
        height=180,
    )
    upsert_vega_raw(
        f"viz-mosaic-{slug}-heat",
        f"{title_pt} — tema x ano",
        vega_heatmap_theme_year_spec(f"{title_pt} — tema x ano", platform),
    )
    upsert_vega_visualization(
        f"viz-mosaic-{slug}-themes",
        f"{title_pt} — top temas",
        "theme",
        platform_filter=platform,
        width=880,
        height=200,
        size=10,
    )
    upsert_multi_panel_dashboard(
        f"dsn-mosaic-{slug}",
        f"DSN Mosaic {title_pt}",
        [
            {"viz_id": f"viz-mosaic-{slug}-line", "x": 0, "y": 0, "w": 32, "h": 12},
            {"viz_id": f"viz-mosaic-{slug}-heat", "x": 32, "y": 0, "w": 16, "h": 12},
            {"viz_id": f"viz-mosaic-{slug}-themes", "x": 0, "y": 12, "w": 48, "h": 12},
        ],
    )


def upsert_mosaic_pattern_c_plataforma():
    """P1 — barras por plataforma + linha + donut (angulo plataforma)."""
    upsert_vega_visualization(
        "viz-mosaic-p1-platforms",
        "Volume por plataforma",
        "platform",
        width=880,
        height=200,
        size=4,
    )
    upsert_vega_raw(
        "viz-mosaic-p1-line",
        "Evolucao total mensal",
        vega_line_global_spec("Evolucao total mensal", width=400, height=200),
    )
    upsert_vega_raw(
        "viz-mosaic-p1-donut",
        "Share por plataforma",
        vega_donut_platform_spec("Share por plataforma"),
    )
    upsert_multi_panel_dashboard(
        "dsn-mosaic-p1",
        "DSN Mosaic P1",
        [
            {"viz_id": "viz-mosaic-p1-platforms", "x": 0, "y": 0, "w": 48, "h": 12},
            {"viz_id": "viz-mosaic-p1-line", "x": 0, "y": 12, "w": 24, "h": 12},
            {"viz_id": "viz-mosaic-p1-donut", "x": 24, "y": 12, "w": 24, "h": 12},
        ],
    )


def upsert_mosaic_eleicao_dashboards():
    upsert_mosaic_theme_pattern_a("eleicao", "Eleicao", "eleicao")


def embed_path(did: str) -> str:
    return f"/app/dashboards#/view/{did}?embed=true&_g={EMBED_G}&hide-filter-bar=true"


def main():
    wait()
    ensure_data_view()
    ensure_index_pattern_so()

    upsert_vega_visualization("viz-dsn-by-theme", "DSN By Theme", "theme")
    upsert_vega_visualization(
        "viz-dsn-theme-engagement", "DSN Theme Engagement", "theme", "sum"
    )
    upsert_vega_visualization("viz-dsn-by-platform", "DSN By Platform", "platform")
    upsert_vega_visualization("viz-dsn-by-platform-year", "DSN By Year", "year")

    upsert_dashboard("dsn-by-theme", "DSN By Theme", "viz-dsn-by-theme")
    upsert_dashboard("dsn-theme-engagement", "DSN Theme Engagement", "viz-dsn-theme-engagement")
    upsert_dashboard("dsn-by-platform", "DSN By Platform", "viz-dsn-by-platform")
    upsert_dashboard("dsn-by-platform-year", "DSN By Year", "viz-dsn-by-platform-year")

    upsert_mosaic_theme_pattern_a("eleicao", "Eleicao", "eleicao")
    upsert_mosaic_theme_pattern_a("vacinas", "Vacinas", "vacinas")
    upsert_mosaic_pattern_c()
    upsert_mosaic_pattern_d()

    upsert_mosaic_pattern_c_plataforma()
    upsert_mosaic_platform_pattern_b("WhatsApp", "WhatsApp", "whatsapp")
    upsert_mosaic_platform_pattern_b("YouTube", "YouTube", "youtube")
    upsert_mosaic_platform_pattern_b("Facebook", "Facebook", "facebook")

    print("\nEmbed URLs (mosaico multi-painel):")
    for did in (
        "dsn-mosaic-t1",
        "dsn-mosaic-eleicao",
        "dsn-mosaic-vacinas",
        "dsn-mosaic-t4",
        "dsn-mosaic-p1",
        "dsn-mosaic-whatsapp",
        "dsn-mosaic-youtube",
        "dsn-mosaic-facebook",
    ):
        print(f"http://localhost:5601{embed_path(did)}")


if __name__ == "__main__":
    main()
