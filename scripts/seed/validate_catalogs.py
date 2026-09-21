"""
TASK-018 — valida catálogos theme/platform no índice.
"""
from __future__ import annotations

import argparse
import json

from es_http import request as es_request
from generate_data import PLATFORMS, THEMES


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--es", default=None)
    parser.add_argument("--index", default="desinfo_events")
    args = parser.parse_args()

    body = {
        "size": 0,
        "aggs": {
            "themes": {"terms": {"field": "theme", "size": 50}},
            "platforms": {"terms": {"field": "platform", "size": 10}},
        },
    }
    _, raw = es_request("POST", f"/{args.index}/_search", body, base=args.es)
    data = json.loads(raw)

    themes = {b["key"] for b in data["aggregations"]["themes"]["buckets"]}
    platforms = {b["key"] for b in data["aggregations"]["platforms"]["buckets"]}
    assert themes == set(THEMES), f"themes mismatch: {themes ^ set(THEMES)}"
    assert platforms == set(PLATFORMS), f"platforms mismatch: {platforms ^ set(PLATFORMS)}"
    print("OK catalogs: 15 themes, 4 platforms")


if __name__ == "__main__":
    main()
