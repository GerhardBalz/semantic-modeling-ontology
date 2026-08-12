# SMO v0.1.0

This is the first governed repository release of the Semantic Modeling Ontology (SMO).

## Semantic contract

SMO v0.1.0 preserves the deliberately minimal initial ontology surface:

- `smo:SemanticModel`;
- `smo:ImplementationProjection`;
- no SMO-owned object properties;
- no SMO-owned datatype properties.

The central invariant remains:

> **Projection or derivation does not transfer semantic authority.**

## Persistent identity

- term namespace: `https://w3id.org/smo#`;
- ontology IRI: `https://w3id.org/smo`;
- version IRI: `https://w3id.org/smo/0.1.0`;
- repository tag: `smo-v0.1.0`.

This release is created only after the current W3ID namespace is active and live resolver verification is green.

## Publication boundary

The repository tag is the immutable source snapshot for subsequent versioned W3ID routing. The release itself does not activate `https://w3id.org/smo/0.1.0`; that route is added only after the immutable release backend exists and is externally verified.

GitHub URLs remain replaceable publication backends rather than SMO semantic identities.

## Included governed artifacts

- `model/smo.ttl`;
- `model/publication-contract.json`;
- `publication/backend-targets.json`;
- `docs/namespace-publication-versioning.md`.

No downstream ESKA or Pizza alignment is part of this release.
