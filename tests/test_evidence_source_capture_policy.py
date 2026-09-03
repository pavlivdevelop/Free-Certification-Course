from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/capture_evidence_sources.py"

spec = importlib.util.spec_from_file_location("capture_evidence_sources", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_http_url_rejects_embedded_credentials() -> None:
    assert not module.http_url("https://user:pass@example.com/path")
    assert module.http_url("https://example.com/path")


def test_public_http_url_accepts_global_ip(monkeypatch) -> None:
    with patch.object(module.socket, "getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))]):
        assert module.public_http_url("https://example.com")


def test_public_http_url_rejects_private_resolution() -> None:
    with patch.object(module.socket, "getaddrinfo", return_value=[(2, 1, 6, "", ("10.0.0.8", 443))]):
        assert not module.public_http_url("https://example.com")


def test_public_http_url_rejects_mixed_resolution() -> None:
    with patch.object(
        module.socket,
        "getaddrinfo",
        return_value=[
            (2, 1, 6, "", ("93.184.216.34", 443)),
            (10, 1, 6, "", ("fc00::8", 443, 0, 0)),
        ],
    ):
        assert not module.public_http_url("https://example.com")
