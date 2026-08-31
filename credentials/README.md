# Credentials layer

This directory is the named-credential layer of the knowledge base.

## Record policy

A record here should name an actual certificate, certification, badge or completion credential issued by an identifiable organization.

### Status classes

- `free` — current official material supports a no-cost credential path.
- `conditional` — no-cost only with a student/educator/voucher/scholarship/campaign/partner condition.
- `paid-reference` — legitimate credential, but the ordinary exam or issuance is paid.
- `review` — provider exists, but the specific free-credential claim needs source verification.

The generator keeps these classes separate from `source-watch` records so a broad provider/domain matrix cannot be mistaken for thousands of real certificates.

## Progress fields

Each generated credential is intended to support a local user state:

`Не начато` → `В процессе` → `Готово` / `Отложено`.

Completion is stored in the browser and can be exported/imported. The catalog itself never stores a person's identity or progress.
