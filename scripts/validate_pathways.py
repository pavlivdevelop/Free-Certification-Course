#!/usr/bin/env python3
"""Deterministic structural validation for the OpenCertAtlas prerequisite graph."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "taxonomy/pathways.json"
ALLOWED_LEVELS = {"Explore", "Beginner", "Foundation", "Intermediate", "Advanced", "Professional", "Expert", "Master"}


def fail(message: str) -> None:
    raise SystemExit(f"PATHWAY ERROR: {message}")


def main() -> int:
    if not PATH.exists():
        fail(f"missing {PATH.relative_to(ROOT)}")
    try:
        doc = json.loads(PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(doc, dict):
        fail("pathways payload must be an object")

    levels = doc.get("levels")
    if not isinstance(levels, list) or not levels:
        fail("levels must be a non-empty list")
    if set(levels) != ALLOWED_LEVELS:
        fail(f"levels mismatch: {levels!r}")

    tracks = doc.get("tracks")
    if not isinstance(tracks, list) or not tracks:
        fail("tracks must be a non-empty list")
    node_levels = doc.get("node_levels")
    if not isinstance(node_levels, dict):
        fail("node_levels must be an object")

    track_ids: set[str] = set()
    all_nodes: set[str] = set()
    edge_count = 0
    for track in tracks:
        if not isinstance(track, dict):
            fail("every track must be an object")
        track_id = str(track.get("id", "")).strip()
        if not track_id:
            fail("track is missing id")
        if track_id in track_ids:
            fail(f"duplicate track id: {track_id!r}")
        track_ids.add(track_id)

        nodes = track.get("nodes")
        edges = track.get("edges")
        if not isinstance(nodes, list) or not nodes:
            fail(f"track {track_id!r} has no nodes")
        if len(nodes) != len(set(nodes)):
            fail(f"track {track_id!r} contains duplicate nodes")
        node_set = {str(n).strip() for n in nodes if str(n).strip()}
        if len(node_set) != len(nodes):
            fail(f"track {track_id!r} contains blank node id")
        all_nodes.update(node_set)
        if not isinstance(edges, list):
            fail(f"track {track_id!r} edges must be a list")

        adjacency = {node: [] for node in node_set}
        for edge in edges:
            if not isinstance(edge, list) or len(edge) != 2:
                fail(f"track {track_id!r} contains malformed edge: {edge!r}")
            src, dst = map(lambda x: str(x).strip(), edge)
            if src not in node_set or dst not in node_set:
                fail(f"track {track_id!r} has dangling edge: {edge!r}")
            if src == dst:
                fail(f"track {track_id!r} has self-loop: {src!r}")
            adjacency[src].append(dst)
            edge_count += 1

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                fail(f"track {track_id!r} contains prerequisite cycle at {node!r}")
            if node in visited:
                return
            visiting.add(node)
            for child in adjacency[node]:
                visit(child)
            visiting.remove(node)
            visited.add(node)

        for node in node_set:
            visit(node)

    missing_levels = sorted(node for node in all_nodes if node not in node_levels)
    if missing_levels:
        fail(f"nodes without node_levels: {missing_levels[:12]!r}")
    invalid_levels = sorted(node for node, level in node_levels.items() if level not in ALLOWED_LEVELS)
    if invalid_levels:
        fail(f"nodes with invalid levels: {invalid_levels[:12]!r}")

    extra_level_nodes = sorted(set(node_levels) - all_nodes)
    if extra_level_nodes:
        fail(f"node_levels contains nodes unused by tracks: {extra_level_nodes[:12]!r}")

    print(f"pathway_tracks={len(tracks)}")
    print(f"pathway_nodes={len(all_nodes)}")
    print(f"pathway_edges={edge_count}")
    print("pathway_validation=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
