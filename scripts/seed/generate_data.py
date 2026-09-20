"""
MOD-SEED — gerador reprodutível de eventos fictícios (desinfo_events).
RNG seed fixa → mesmos dados (US-017 / TASK-003).
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

PLATFORMS = ["WhatsApp", "Facebook", "Instagram", "YouTube"]
THEMES = [
    "eleicao",
    "governo",
    "vacinas",
    "saude",
    "educacao",
    "economia",
    "seguranca",
    "meio_ambiente",
    "religiao",
    "genero",
    "imigracao",
    "ciencia",
    "midia",
    "justica",
    "outros",
]
UFS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]
YEARS = [2021, 2022, 2023, 2024]

FAKE_TOWNS = [
    "Vila Exemplo", "Campo Demo", "Praia Sintetica", "Serra Ficticia",
    "Lago Modelo", "Vale Simulado", "Centro Amostra", "Bairro Seed",
]


def _weighted_choice(rng: random.Random, items: list[Any], weights: list[float]) -> Any:
    return rng.choices(items, weights=weights, k=1)[0]


def _theme_weights(year: int) -> list[float]:
    w = [1.0] * len(THEMES)
    idx_eleicao = THEMES.index("eleicao")
    idx_vacinas = THEMES.index("vacinas")
    if year == 2022:
        w[idx_eleicao] = 4.5
    if year == 2021:
        w[idx_vacinas] = 4.0
    return w


def _year_weights() -> list[float]:
    # leve viés para 2022 (eleição) e 2021 (vacinas)
    return [1.4, 1.6, 1.1, 1.0]


def generate_events(n: int = 50_000, rng_seed: int = 42) -> list[dict[str, Any]]:
    rng = random.Random(rng_seed)
    events: list[dict[str, Any]] = []
    for i in range(n):
        year = _weighted_choice(rng, YEARS, _year_weights())
        theme = _weighted_choice(rng, THEMES, _theme_weights(year))
        platform = rng.choice(PLATFORMS)
        uf = rng.choice(UFS)
        day = rng.randint(1, 28)
        month = rng.randint(1, 12)
        hour = rng.randint(0, 23)
        minute = rng.randint(0, 59)
        ts = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
        # jitter seconds
        ts = ts + timedelta(seconds=rng.randint(0, 59))
        events.append(
            {
                "event_id": f"evt-{year}-{i:06d}",
                "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "year": year,
                "platform": platform,
                "theme": theme,
                "uf": uf,
                "municipality_fake": rng.choice(FAKE_TOWNS),
                "engagement_count": int(rng.lognormvariate(5.5, 1.1)),
                "narrative_label": f"rumor_{theme}_{rng.randint(1, 40)}",
                "source_channel_fake": f"canal_demo_{rng.randint(1, 80):02d}",
            }
        )
    return events


def write_sample(events: list[dict[str, Any]], path: Path, n: int = 100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events[:n], ensure_ascii=False, indent=2), encoding="utf-8")


def write_ndjson(events: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera seed fictício desinfo_events")
    parser.add_argument("--n", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--sample", type=Path, default=Path("data/sample.json"))
    parser.add_argument("--out", type=Path, default=Path("data/generated/desinfo_events.ndjson"))
    parser.add_argument("--csv-shiny", type=Path, default=Path("data/generated/shiny_seed.csv"))
    args = parser.parse_args()

    events = generate_events(n=args.n, rng_seed=args.seed)
    write_sample(events, args.sample, n=100)
    write_ndjson(events, args.out)

    # CSV enxuto para Shiny (amostra agregável)
    import csv

    args.csv_shiny.parent.mkdir(parents=True, exist_ok=True)
    with args.csv_shiny.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "event_id",
                "year",
                "platform",
                "theme",
                "uf",
                "engagement_count",
            ],
        )
        w.writeheader()
        for e in events[::10]:  # 5k linhas para Shiny
            w.writerow({k: e[k] for k in w.fieldnames})

    print(f"Generated {len(events)} events (seed={args.seed})")
    print(f"Sample -> {args.sample}")
    print(f"NDJSON -> {args.out}")
    print(f"Shiny CSV -> {args.csv_shiny}")


if __name__ == "__main__":
    main()
