# Namespace, publication, and versioning contract

## Status

The SMO publication contract is **pre-activation**. This repository prepares the namespace and backend payload but does not claim that W3ID routing is live.

No W3ID request, release, or tag is created by the v0.1 bootstrap.

## Semantic identity

The prepared term namespace is:

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

GitHub repository and raw-content URLs are publication backends only. They are not semantic identifiers and must not appear as SMO term or ontology identity.

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

## Publication staging

Publication is intentionally staged:

1. maintain the governed repository baseline;
2. define the ontology and machine-readable publication contract;
3. verify the ontology, namespace, and prepared backend targets in CI;
4. prepare the W3ID redirect payload;
5. review and merge the repository baseline;
6. create the governed `smo-v0.1.0` release/tag when the publication baseline is approved;
7. request `w3id.org/smo` activation;
8. verify live current and immutable version routes externally;
9. only then align downstream vocabularies such as ESKA and Pizza.

The exact release/W3ID ordering may be performed as one publication change set, but a version route must never be advertised as live before its immutable backend exists.

## Prepared backend targets

`publication/backend-targets.json` records the planned current and immutable targets. `publication/w3id/.htaccess` contains the corresponding W3ID payload.

Both artifacts are explicitly marked pre-activation. A raw GitHub target is transport infrastructure, not an ontology IRI.

## Versioning

The initial semantic version is `0.1.0`.

The planned repository tag pattern is:

```text
smo-v{version}
```

The initial immutable tag will therefore be `smo-v0.1.0`, but the bootstrap does not create it.

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
8. prepared W3ID targets point to this governed repository and remain explicitly inactive;
9. this documentation and the README state the same namespace/version/pre-activation contract.

Repository publication additionally requires the GitHub repository to be public with the approved description before W3ID activation.
