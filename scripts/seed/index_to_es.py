"""
MOD-SEED / MOD-ES — cria índice desinfo_events e faz bulk (TASK-002 / TASK-003).
Acesso ES: localhost se publicado; senão docker exec (BUG-004).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from es_http import request as es_request
from es_http import wait_ready

MAPPING = {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
        "properties": {
            "event_id": {"type": "keyword"},
            "timestamp": {"type": "date"},
            "year": {"type": "integer"},
            "platform": {"type": "keyword"},
            "theme": {"type": "keyword"},
            "uf": {"type": "keyword"},
            "municipality_fake": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            "engagement_count": {"type": "long"},
            "narrative_label": {"type": "keyword"},
            "source_channel_fake": {"type": "keyword"},
        }
    },
}

INDEX = "desinfo_events"


def create_index(base: str, recreate: bool = False) -> None:
    if recreate:
        try:
            es_request("DELETE", f"/{INDEX}", base=base)
        except Exception:
            pass
    status, raw = es_request("PUT", f"/{INDEX}", MAPPING, base=base)
    print("create_index", status, raw[:200])


def bulk_index(base: str, ndjson_path: Path, batch_size: int = 2000) -> int:
    total = 0
    batch: list[str] = []

    def flush() -> None:
        nonlocal total, batch
        if not batch:
            return
        payload = "".join(batch).encode("utf-8")
        es_request(
            "POST",
            "/_bulk",
            payload,
            base=base,
            content_type="application/x-ndjson",
        )
        total += len(batch) // 2
        batch = []

    with ndjson_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            doc = json.loads(line)
            meta = {"index": {"_index": INDEX, "_id": doc["event_id"]}}
            batch.append(json.dumps(meta) + "\n")
            batch.append(json.dumps(doc) + "\n")
            if len(batch) >= batch_size * 2:
                flush()
        flush()
    es_request("POST", f"/{INDEX}/_refresh", base=base)
    return total


def count_docs(base: str) -> int:
    _, raw = es_request("GET", f"/{INDEX}/_count", base=base)
    data = json.loads(raw)
    return int(data.get("count", 0))


def validate_aggs(base: str) -> None:
    query = {
        "size": 0,
        "aggs": {
            "by_platform": {"terms": {"field": "platform", "size": 10}},
            "by_year": {"terms": {"field": "year", "size": 10}},
            "by_uf": {"terms": {"field": "uf", "size": 30}},
            "by_theme": {"terms": {"field": "theme", "size": 20}},
        },
    }
    _, raw = es_request("POST", f"/{INDEX}/_search", query, base=base)
    data = json.loads(raw)
    for key in ("by_platform", "by_year", "by_uf", "by_theme"):
        buckets = data["aggregations"][key]["buckets"]
        assert buckets, f"agregação vazia: {key}"
        print(key, len(buckets), "buckets — top:", buckets[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--es", default=None, help="Base URL (opcional; fallback docker exec)")
    parser.add_argument("--ndjson", type=Path, default=Path("data/generated/desinfo_events.ndjson"))
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("--skip-bulk", action="store_true")
    args = parser.parse_args()

    base = wait_ready(args.es)
    # recreate may hit "already exists" — retry once
    try:
        create_index(base, recreate=args.recreate)
    except Exception as e:
        if "resource_already_exists" in str(e).lower() or "400" in str(e):
            print("index already exists")
        else:
            # PUT may return 400 via docker; try ignore
            print("create_index note:", e)
            time.sleep(1)
            create_index(base, recreate=False)

    if not args.skip_bulk:
        if not args.ndjson.is_file():
            print("NDJSON ausente. Rode: python scripts/seed/generate_data.py", file=sys.stderr)
            sys.exit(1)
        n = bulk_index(base, args.ndjson)
        print(f"bulk indexed ~{n} actions")
    print("count", count_docs(base))
    validate_aggs(base)


if __name__ == "__main__":
    main()
