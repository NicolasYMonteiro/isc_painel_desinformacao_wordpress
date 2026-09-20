"""
TASK-018 — valida catálogos theme/platform no índice.
"""
from __future__ import annotations

import argparse
import json
import urllib.request

from generate_data import PLATFORMS, THEMES


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--es", default="http://localhost:9200")
    parser.add_argument("--index", default="desinfo_events")
    args = parser.parse_args()

    body = json.dumps(
        {
            "size": 0,
            "aggs": {
                "themes": {"terms": {"field": "theme", "size": 50}},
                "platforms": {"terms": {"field": "platform", "size": 10}},
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{args.es}/{args.index}/_search",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())

    themes = {b["key"] for b in data["aggregations"]["themes"]["buckets"]}
    platforms = {b["key"] for b in data["aggregations"]["platforms"]["buckets"]}
    assert themes == set(THEMES), f"themes mismatch: {themes ^ set(THEMES)}"
    assert platforms == set(PLATFORMS), f"platforms mismatch: {platforms ^ set(PLATFORMS)}"
    print("OK catalogs: 15 themes, 4 platforms")


if __name__ == "__main__":
    main()
