"""
Cliente HTTP para Elasticsearch.

Preferência: DSN_ES_URL / localhost:9200.
Fallback (BUG-004 / RNF-009): docker exec no container dsn-elasticsearch
quando a porta 9200 não está publicada no host.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

ES_DEFAULT = os.environ.get("DSN_ES_URL", "http://localhost:9200").rstrip("/")
ES_CONTAINER = os.environ.get("DSN_ES_CONTAINER", "dsn-elasticsearch")


def _direct(method: str, url: str, body: bytes | None, content_type: str, timeout: int):
    headers = {"Content-Type": content_type} if body is not None else {}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def _docker(method: str, path: str, body: bytes | None, content_type: str, timeout: int):
    cmd = [
        "docker",
        "exec",
        "-i",
        ES_CONTAINER,
        "curl",
        "-sS",
        "-w",
        "\n__STATUS__%{http_code}",
        "-X",
        method,
        f"http://127.0.0.1:9200{path}",
        "--max-time",
        str(timeout),
    ]
    if body is not None:
        cmd.extend(["-H", f"Content-Type: {content_type}", "--data-binary", "@-"])
    proc = subprocess.run(
        cmd,
        input=body,
        capture_output=True,
        timeout=timeout + 30,
    )
    if proc.returncode != 0:
        err = (proc.stderr or b"").decode("utf-8", errors="replace")
        raise urllib.error.URLError(f"docker exec curl failed: {err}")
    raw = proc.stdout
    marker = b"\n__STATUS__"
    idx = raw.rfind(marker)
    if idx < 0:
        raise urllib.error.URLError("docker exec curl: missing status marker")
    payload = raw[:idx]
    status = int(raw[idx + len(marker) :].decode("ascii").strip())
    return status, payload


def request(
    method: str,
    path: str,
    body: bytes | dict | None = None,
    *,
    base: str | None = None,
    content_type: str = "application/json",
    timeout: int = 120,
) -> tuple[int, bytes]:
    base_url = (base or ES_DEFAULT).rstrip("/")
    if isinstance(body, dict):
        body = json.dumps(body).encode("utf-8")
    if not path.startswith("/"):
        path = "/" + path
    url = f"{base_url}{path}"
    try:
        return _direct(method, url, body, content_type, timeout)
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        return _docker(method, path, body, content_type, timeout)


def search(body: dict, *, index: str = "desinfo_events", base: str | None = None) -> dict[str, Any]:
    status, raw = request("POST", f"/{index}/_search", body, base=base)
    if status >= 400:
        raise RuntimeError(f"ES search {status}: {raw[:300]!r}")
    return json.loads(raw.decode("utf-8"))


def wait_ready(base: str | None = None, attempts: int = 90) -> str:
    base_url = (base or ES_DEFAULT).rstrip("/")
    for i in range(attempts):
        try:
            status, _ = request("GET", "/_cluster/health", base=base_url, timeout=5)
            if status == 200:
                print(f"OK Elasticsearch ({base_url} ou docker exec)")
                return base_url
        except Exception:
            pass
        print(f"  waiting Elasticsearch ({i + 1}/{attempts})...")
        time.sleep(3)
    raise SystemExit("Timeout aguardando Elasticsearch")


def host_port_published(port: int = 9200) -> bool:
    """True se algo responde em localhost:port (útil para asserts RNF-009)."""
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2)
        return True
    except Exception:
        return False
