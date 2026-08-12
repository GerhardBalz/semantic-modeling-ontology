# Namespace, publication, and versioning contract

## Status

The SMO publication state is **version-active**.

The current W3ID namespace was activated through `perma-id/w3id.org` PR #6538, merged as upstream commit:

```text
42367a77c52b60dab4cdf55327fca023e78a61a4
```

Current-route live verification succeeded in GitHub Actions run:

```text
https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31627245287
```

The first governed immutable repository release exists as:

```text
release tag      smo-v0.1.0
release commit   e6ab3f8cf14bafae466a0150ad356547f164bdab
publisher run    https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31633781524
release          https://github.com/GerhardBalz/semantic-modeling-ontology/releases/tag/smo-v0.1.0
```

The immutable W3ID version route was activated through `perma-id/w3id.org` PR #6541, merged as:

```text
84d541d959006ea6df14014e880020223c3c059b
```

The hardened verifier merged as:

```text
e9422be4aa01e8889bb11b6e4dc38348c4e55a98
```

and current + immutable live verification succeeded in:

```text
https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31642224022
```

That run observed the internal W3ID canonicalization hop for the bare namespace, then verified the governed terminal targets for current HTML/Turtle/distribution and immutable v0.1.0 HTML/Turtle/distribution routes.

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
release-published
    ↓ submit + merge immutable version route + live verification
version-active                ← current state
```

A stage may only be claimed after its observable condition is satisfied.

## Current active routes

W3ID PR #6538 governs current routes:

- browser requests for `https://w3id.org/smo` → governed SMO repository;
- Turtle requests for `https://w3id.org/smo` → current authoritative `main/model/smo.ttl`;
- `/docs` → namespace/publication documentation;
- `/dist/smo.ttl` → current authoritative Turtle.

The live verifier permits internal `w3id.org` canonicalization (currently the bare namespace returns a 301 to the slash form) but requires the terminal external W3ID redirect to be the governed backend target.

## Immutable v0.1.0 routes

W3ID PR #6541 governs the immutable version routes:

- browser requests for `https://w3id.org/smo/0.1.0` → tagged `smo-v0.1.0/model/smo.ttl` on GitHub;
- Turtle requests for `https://w3id.org/smo/0.1.0` → tagged raw `smo-v0.1.0/model/smo.ttl`;
- `https://w3id.org/smo/0.1.0/dist/smo.ttl` → tagged raw `smo-v0.1.0/model/smo.ttl`.

Every immutable route targets the governed release tag `smo-v0.1.0`, never mutable `main`.

The governed immutable release backend is:

```text
https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl
```

The tag `smo-v0.1.0` points exactly to:

```text
e6ab3f8cf14bafae466a0150ad356547f164bdab
```

## Verification model

`publication/verify-live-w3id.py` separates two concerns:

1. W3ID redirect governance: follow only internal `w3id.org` canonicalization hops, stop before external backends, and require the terminal redirect to match the governed target;
2. semantic backend evidence: fetch the authoritative Turtle target independently, parse it, verify the two SMO classes, and for v0.1.0 verify the declared version IRI and version info.

Transient network disconnects are retried with a bounded policy; semantic, redirect-target, or HTTP-contract failures are not hidden by retries.

## Next governed transition

The publication and persistent-identity sequence for SMO v0.1.0 is complete. The next activity is SMO #11: evaluate downstream alignment in ESKA and Pizza using the now-durable SMO current and immutable identities.

Analysis must still precede semantic changes. In particular, do not modify immutable `smo-v0.1.0`, immutable `eska-v0.1.0`, or historical Pizza semantics merely to create symmetry.

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
8. W3ID PR #6538 and its current-route merge/live evidence are recorded;
9. `smo-v0.1.0` and its exact governed release commit are recorded;
10. the immutable tagged backend is recorded as verified;
11. W3ID PR #6541 and its immutable-route merge/live evidence are recorded;
12. both current and immutable W3ID routes are marked active only with successful live-verification evidence;
13. this documentation and the README state the same `version-active` contract.

## Downstream gate

The persistent-publication gate is now satisfied. SMO #11 may proceed with analysis of ESKA/Pizza alignment.

This does not authorize automatic semantic convergence. Any downstream change must preserve source ownership, avoid modifying immutable releases, and be justified by concrete modeling evidence.
