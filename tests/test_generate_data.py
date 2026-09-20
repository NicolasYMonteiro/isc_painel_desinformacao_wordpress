"""TEST-001 / TEST-003 — testes do gerador de seed (TDD)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "seed"))

from generate_data import (  # noqa: E402
    PLATFORMS,
    THEMES,
    UFS,
    YEARS,
    generate_events,
)


RNG_SEED = 42
TARGET_N = 50_000


def test_generate_count():
    events = generate_events(n=TARGET_N, rng_seed=RNG_SEED)
    assert len(events) == TARGET_N


def test_generate_reproducible():
    a = generate_events(n=1000, rng_seed=RNG_SEED)
    b = generate_events(n=1000, rng_seed=RNG_SEED)
    assert a == b


def test_generate_different_seeds_differ():
    a = generate_events(n=500, rng_seed=1)
    b = generate_events(n=500, rng_seed=2)
    assert a != b


def test_catalog_coverage_in_large_sample():
    events = generate_events(n=TARGET_N, rng_seed=RNG_SEED)
    platforms = {e["platform"] for e in events}
    themes = {e["theme"] for e in events}
    ufs = {e["uf"] for e in events}
    years = {e["year"] for e in events}
    assert platforms == set(PLATFORMS)
    assert themes == set(THEMES)
    assert ufs == set(UFS)
    assert years == set(YEARS)


def test_no_pii_fields():
    events = generate_events(n=100, rng_seed=RNG_SEED)
    forbidden = {"email", "cpf", "phone", "nome_real", "ssn"}
    for e in events:
        assert forbidden.isdisjoint(e.keys())
        assert "event_id" in e
        assert e["platform"] in PLATFORMS
        assert e["theme"] in THEMES


def test_required_schema_fields():
    e = generate_events(n=1, rng_seed=RNG_SEED)[0]
    required = {
        "event_id",
        "timestamp",
        "year",
        "platform",
        "theme",
        "uf",
        "engagement_count",
        "narrative_label",
        "source_channel_fake",
    }
    assert required.issubset(e.keys())


def test_election_2022_and_vaccines_2021_boosted():
    events = generate_events(n=TARGET_N, rng_seed=RNG_SEED)
    eleicao_2022 = sum(1 for e in events if e["theme"] == "eleicao" and e["year"] == 2022)
    vacinas_2021 = sum(1 for e in events if e["theme"] == "vacinas" and e["year"] == 2021)
    baseline = TARGET_N / (len(THEMES) * len(YEARS))
    assert eleicao_2022 > baseline * 1.5
    assert vacinas_2021 > baseline * 1.5
