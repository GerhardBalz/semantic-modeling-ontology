# Namespace, publication, and versioning contract

## Status

The SMO current publication state is **current-active**.

The current W3ID namespace was activated through `perma-id/w3id.org` PR #6538, merged as upstream commit:

```text
42367a77c52b60dab4cdf55327fca023e78a61a4
```

Live resolver verification then succeeded in GitHub Actions run:

```text
https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31627245287
```

That run verified HTML resolution, Turtle content negotiation, the explicit Turtle distribution route, and the presence of `smo:SemanticModel` and `smo:ImplementationProjection` in live RDF.

No `smo-v0.1.0` release/tag exists yet, and no immutable `0.1.0` W3ID route is active.

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
current-active              ← current state
    ↓ create governed smo-v0.1.0 release
release-published
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

## Prepared backend targets

`publication/backend-targets.json` records both the active current target and the planned immutable target.

The planned immutable route targets:

```text
https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl
```

and therefore cannot become active before `smo-v0.1.0` exists.

## Next governed transitions

1. publish the governed `smo-v0.1.0` release/tag from the active current baseline;
2. verify the immutable backend publicly;
3. submit immutable W3ID routes for `https://w3id.org/smo/0.1.0`;
4. verify current and immutable routes together;
5. only then execute downstream SMO #11 alignment in ESKA and Pizza.

## Versioning

The initial semantic version is `0.1.0`.

The repository tag pattern is:

```text
smo-v{version}
```

The initial immutable tag will therefore be:

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
10. the immutable route remains inactive before `smo-v0.1.0` exists;
11. this documentation and the README state the same current-active contract.

## Downstream gate

SMO #11 deliberately remains blocked while immutable publication is incomplete.

Do not yet:

- modify ESKA `SemanticModel` compatibility;
- add SMO typing to Pizza as a canonical dependency;
- mark `eska:SemanticModel` deprecated;
- change immutable `eska-v0.1.0`.

Current + immutable publication evidence is the gate that makes downstream cross-repository references durable rather than provisional.
