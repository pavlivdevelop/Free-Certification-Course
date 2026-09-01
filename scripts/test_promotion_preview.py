#!/usr/bin/env python3
"""Small deterministic regression tests for promotion-preview identity triage."""
from __future__ import annotations

from promotion_preview import credential_identity_signals


def assert_signal(name: str, url: str, expected_triage: str, expected_delta: int) -> None:
    delta, triage, reasons = credential_identity_signals(name, url)
    assert triage == expected_triage, (name, triage, reasons)
    assert delta == expected_delta, (name, delta, reasons)


def main() -> int:
    assert_signal(
        "AWS Certified Cloud Practitioner",
        "https://aws.amazon.com/certification/certified-cloud-practitioner/",
        "likely credential identity",
        1,
    )
    assert_signal(
        "Apache Kafka® 101 - Introduction",
        "https://developer.confluent.io/courses/apache-kafka/events/",
        "learning-content signal",
        -6,
    )
    assert_signal(
        "AI For Everyone",
        "https://www.coursera.org/learn/ai-for-everyone",
        "learning-content signal",
        -3,
    )
    assert_signal(
        "Cloud Architecture Foundations",
        "https://example.org/catalog/cloud-architecture-foundations",
        "uncertain credential identity",
        0,
    )
    print("promotion_preview_identity_tests=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
