# OpenCertAtlas Recommendation Model

The recommendation page is intentionally deterministic and local-first. It does not claim to be an AI career adviser.

## Inputs

- user-selected goal/domain;
- optional target level;
- optional free-only filter;
- locally stored completion state;
- catalog fields already present in `data/catalog-expanded.json`.

## Ranking signals

1. Goal/domain match.
2. Target level match.
3. `✅ Free` preference when selected.
4. `credential` record type over discovery/reference records.
5. Presence of official-page extraction evidence.
6. Normalized level proximity.

## Safety boundary

A recommendation never upgrades a record's `Record Type`, price status or verification state. Unknown and candidate records remain visibly marked.

## Progress storage

Progress is stored locally under `oca-progress`. Exported files use `opencertatlas-progress.json`. The recommender reads the same state model as the progress tracker and tolerates the legacy flat map during migration.

## Future evolution

The next generation can consume explicit prerequisite edges from `taxonomy/` and evidence confidence from `evidence/`, replacing heuristic matching with a deterministic directed learning graph.
