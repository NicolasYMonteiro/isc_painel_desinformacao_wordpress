"""
MOD-SEED / MOD-ES — cria índice desinfo_events e faz bulk (TASK-002 / TASK-003).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

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


def _req(method: str, url: str, body: bytes | None = None, content_type: str = "application/json"):
    headers = {"Content-Type": content_type} if body is not None else {}
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=120) as resp:
        return resp.status, resp.read()


def wait_es(base: str, attempts: int = 60) -> None:
    for i in range(attempts):
        try:
            status, _ = _req("GET", f"{base}/_cluster/health")
            if status == 200:
                return
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(2)
    raise RuntimeError(f"Elasticsearch não respondeu em {base}")


def create_index(base: str, recreate: bool = False) -> None:
    url = f"{base}/{INDEX}"
    if recreate:
        try:
            _req("DELETE", url)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
    body = json.dumps(MAPPING).encode("utf-8")
    try:
        status, raw = _req("PUT", url, body)
        print("create_index", status, raw[:200])
    except urllib.error.HTTPError as e:
        if e.code == 400 and b"resource_already_exists" in e.read():
            print("index already exists")
        else:
            raise


def bulk_index(base: str, ndjson_path: Path, batch_size: int = 2000) -> int:
    total = 0
    batch: list[str] = []

    def flush() -> None:
        nonlocal total, batch
        if not batch:
            return
        payload = "".join(batch).encode("utf-8")
        _req("POST", f"{base}/_bulk", payload, content_type="application/x-ndjson")
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
    # refresh
    _req("POST", f"{base}/{INDEX}/_refresh")
    return total


def count_docs(base: str) -> int:
    status, raw = _req("GET", f"{base}/{INDEX}/_count")
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
    body = json.dumps(query).encode("utf-8")
    _, raw = _req("POST", f"{base}/{INDEX}/_search", body)
    data = json.loads(raw)
    for key in ("by_platform", "by_year", "by_uf", "by_theme"):
        buckets = data["aggregations"][key]["buckets"]
        assert buckets, f"agregação vazia: {key}"
        print(key, len(buckets), "buckets — top:", buckets[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--es", default="http://localhost:9200")
    parser.add_argument("--ndjson", type=Path, default=Path("data/generated/desinfo_events.ndjson"))
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("--skip-bulk", action="store_true")
    args = parser.parse_args()

    wait_es(args.es)
    create_index(args.es, recreate=args.recreate)
    if not args.skip_bulk:
        if not args.ndjson.is_file():
            print("NDJSON ausente. Rode: python scripts/seed/generate_data.py", file=sys.stderr)
            sys.exit(1)
        n = bulk_index(args.es, args.ndjson)
        print(f"bulk indexed ~{n} actions")
    print("count", count_docs(args.es))
    validate_aggs(args.es)


if __name__ == "__main__":
    main()
