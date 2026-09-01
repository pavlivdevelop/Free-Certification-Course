# Methodology

## Status model

`free` means the issuer currently presents the credential or credential-bearing activity as free under normal access conditions.

`conditional` means a free route exists, but it depends on a student/educator status, voucher, scholarship, campaign, partner programme, or a course-specific condition.

`paid-reference` means the professional exam is normally paid. These rows are retained only as career-reference targets and are excluded from the free core.

## Evidence model

Each row should keep:

- official issuer URL;
- credential name exactly as issued;
- credential type (certification, certificate, badge, applied skill, completion record);
- current price status;
- eligibility/geo caveats;
- verification method when published by the issuer;
- date of last review.

## Evidence promotion boundary

Extracted or discovered records remain `credential-candidate` until evidence is reviewed. The promotion preview is a deterministic prioritization aid for human review; its score is not evidence and it cannot change canonical records, verification state, or free status.

A manual promotion decision should confirm, from the issuer source, all of the following before changing `Evidence Status` or entering the free core:

1. the exact credential identity is real and issuer-owned;
2. the activity is credential-bearing rather than a generic course or marketing page;
3. the current access or assessment route supports the claimed price status;
4. eligibility, geography, and important conditions are captured;
5. the source page and review date are recorded.

A high preview score only means that the row is well formed for inspection. It does not establish that any of these claims are true.

## Safety against stale information

Prices, exam versions, retirements and country availability change. A repository row is a directory record, not a promise that an issuer will keep the same offer forever. Before spending money, submitting identity data, or planning a credential into a formal application, verify the current issuer page.

## Scope

The repository is intentionally broader than software. It includes engineering, hardware, electronics, RF, embedded, robotics, automation, manufacturing, energy, automotive, aerospace, GIS, telecom, quantum, mathematics, physics, biotech, healthcare, environment, finance, logistics, business technology and other fields where credible learning credentials exist.
