# Namespace, publication, and versioning contract

## Status

The SMO publication state is **release-published**.

The current W3ID namespace was activated through `perma-id/w3id.org` PR #6538, merged as upstream commit:

```text
42367a77c52b60dab4cdf55327fca023e78a61a4
```

Live resolver verification then succeeded in GitHub Actions run:

```text
https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31627245287
```

The first governed immutable repository release now exists:

```text
release tag      smo-v0.1.0
release commit   e6ab3f8cf14bafae466a0150ad356547f164bdab
publisher run    https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31633781524
release          https://github.com/GerhardBalz/semantic-modeling-ontology/releases/tag/smo-v0.1.0
```

The tagged `model/smo.ttl` backend is fetchable under `smo-v0.1.0`. The immutable `https://w3id.org/smo/0.1.0` route is not active yet.

## Semantic identity

The term namespace is:

```text
https://w3id.org/smo#
```

The ontology IRI is:

```text
https://w3id.org/smo
```

The initial ontology version is `0.1.0`, with version IRI:

```text
https://w3id.org/smo/0.1.0
```

SMO term IRIs are unversioned. Version IRIs identify immutable ontology versions; they do not replace the stable term namespace.

GitHub repository and raw-content URLs are publication backends only. They are not semantic identifiers.

## v0.1 conceptual boundary

Version 0.1 owns exactly two classes:

```text
smo:SemanticModel
smo:ImplementationProjection
```

No SMO-owned relation is introduced in v0.1. Implementations should use established vocabularies for evidence that already has standardized semantics, including:

- PROV-O for derivation, usage, and roles;
- Dublin Core Terms for source, relation, conformance, and descriptive metadata;
- DCAT for actual publication and distribution resources;
- OWL/RDFS for ontology and class semantics.

The architectural invariant is that an implementation projection is non-authoritative for the semantics it projects. Derivation or projection does not by itself transfer semantic authority.

## Publication state machine

```text
pre-activation
    ↓ upstream W3ID request submitted
activation-requested
    ↓ upstream merge + external HTML/Turtle verification
current-active
    ↓ create governed smo-v0.1.0 release
release-published            ← current state
    ↓ submit + merge immutable version route
version-active
```

A stage may only be claimed after its observable condition is satisfied.

## Current active routes

W3ID PR #6538 activates current routes only:

- browser requests for `https://w3id.org/smo` → governed SMO repository;
- Turtle requests for `https://w3id.org/smo` → current authoritative `main/model/smo.ttl`;
- `/docs` → namespace/publication documentation;
- `/dist/smo.ttl` → current authoritative Turtle.

It deliberately contains no `0.1.0` version route.

## Governed immutable backend

The governed immutable release backend now exists at:

```text
https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl
```

The tag `smo-v0.1.0` points exactly to:

```text
e6ab3f8cf14bafae466a0150ad356547f164bdab
```

`publication/backend-targets.json` records that backend as release-backed and verified, while keeping the W3ID version route inactive until the separate upstream activation is complete.

## Next governed transitions

1. prepare the immutable W3ID route payload under SMO #10;
2. submit an upstream W3ID change for `https://w3id.org/smo/0.1.0` targeting only `smo-v0.1.0`;
3. after upstream merge, verify current and immutable routes together;
4. advance the machine state to `version-active` only after that external verification succeeds;
5. only then execute downstream SMO #11 alignment in ESKA and Pizza.

## Versioning

The initial semantic version is `0.1.0`.

The repository tag pattern is:

```text
smo-v{version}
```

The first governed immutable tag is:

```text
smo-v0.1.0
```

Compatibility guidance for later versions:

- patch: documentation, annotations, metadata, or corrections that do not change intended machine-interpretable meaning;
- minor: backward-compatible additive semantic changes;
- major: breaking semantic-contract changes.

## Acceptance contract

`model/verify-model.py` is the executable acceptance contract. CI must prove that:

1. `model/smo.ttl` parses as Turtle;
2. ontology IRI, version, and version IRI match `model/publication-contract.json`;
3. exactly the intended two SMO-owned classes are declared;
4. both definitions are present with consistent English language tags;
5. no SMO-owned object or datatype property is introduced;
6. no accidental ESKA execution, capability, service, agent, result, verification, or deployment vocabulary enters SMO;
7. no GitHub repository URL becomes semantic identity;
8. W3ID PR #6538 and its merge commit are recorded;
9. current publication is marked active only with successful live-verification evidence;
10. `smo-v0.1.0` and its exact governed release commit are recorded;
11. the immutable tagged backend is recorded as verified;
12. the immutable W3ID route remains inactive until its separate upstream activation succeeds;
13. this documentation and the README state the same `release-published` contract.

## Downstream gate

SMO #11 deliberately remains blocked while immutable W3ID publication is incomplete.

Do not yet:

- modify ESKA `SemanticModel` compatibility;
- add SMO typing to Pizza as a canonical dependency;
- mark `eska:SemanticModel` deprecated;
- change immutable `eska-v0.1.0`.

Current + immutable W3ID publication evidence is the gate that makes downstream cross-repository references durable rather than provisional.
