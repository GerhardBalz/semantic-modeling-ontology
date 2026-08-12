# Namespace, publication, and versioning contract

## Status

The SMO publication contract is **activation-requested**.

The initial current-route request has been submitted upstream as:

```text
perma-id/w3id.org PR #6538
https://github.com/perma-id/w3id.org/pull/6538
```

The PR is not yet merged. Therefore this repository does **not** claim that `https://w3id.org/smo` is live, and the machine-readable route metadata remains `active: false`.

No `smo-v0.1.0` release/tag exists yet, and no immutable `0.1.0` W3ID route has been requested.

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

SMO publication is intentionally explicit about observable transitions:

```text
pre-activation
    ↓ upstream W3ID request submitted
activation-requested        ← current state
    ↓ upstream merge + external HTML/Turtle verification
current-active
    ↓ create governed smo-v0.1.0 release
release-published
    ↓ submit + merge immutable version route
version-active
```

A stage may only be claimed after its observable condition is satisfied.

### Current transition

W3ID PR #6538 contains only current routes:

- browser requests for `https://w3id.org/smo` → governed SMO repository;
- Turtle requests for `https://w3id.org/smo` → current authoritative `main/model/smo.ttl`;
- `/docs` → namespace/publication documentation;
- `/dist/smo.ttl` → current authoritative Turtle.

It deliberately contains no `0.1.0` version route.

## Prepared backend targets

`publication/backend-targets.json` records both current and planned immutable targets.

The current route records W3ID PR #6538 as its activation request but remains inactive until upstream merge and external verification.

The planned immutable route targets:

```text
https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl
```

and therefore cannot become active before `smo-v0.1.0` exists.

The submitted W3ID payload under `publication/w3id/` remains the current-route activation payload. Its pre-activation wording describes the resolver state of that payload before upstream activation and does not assert that the request itself has not been submitted.

## Next steps after W3ID merge

When PR #6538 merges:

1. verify `https://w3id.org/smo` externally as HTML;
2. verify Turtle content negotiation externally;
3. verify returned RDF contains `https://w3id.org/smo#SemanticModel` and `https://w3id.org/smo#ImplementationProjection`;
4. make live resolver verification executable in CI;
5. update `w3idActive` and the current route only after those checks pass;
6. create the governed `smo-v0.1.0` release/tag;
7. add immutable W3ID routes for `https://w3id.org/smo/0.1.0`;
8. verify current and immutable routes together;
9. only then execute downstream SMO #11 alignment in ESKA and Pizza.

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
8. the W3ID request is recorded as submitted through PR #6538;
9. neither current nor immutable route is claimed active prematurely;
10. no release is claimed before `smo-v0.1.0` exists;
11. this documentation and the README state the same activation-requested contract.

## Downstream gate

SMO #11 deliberately remains blocked while publication is incomplete.

Do not yet:

- modify ESKA `SemanticModel` compatibility;
- add SMO typing to Pizza as a canonical dependency;
- mark `eska:SemanticModel` deprecated;
- change immutable `eska-v0.1.0`.

The live namespace and immutable v0.1.0 evidence are the gate that makes downstream cross-repository references durable rather than provisional.
