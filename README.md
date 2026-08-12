# Semantic Modeling Ontology (SMO)

A small, standards-aligned ontology for authoritative semantic models and their non-authoritative implementation projections.

> **Status:** `activation-requested` for v0.1 publication. The current SMO W3ID namespace request is submitted as [`perma-id/w3id.org#6538`](https://github.com/perma-id/w3id.org/pull/6538), but the namespace is **not yet claimed active** and no `smo-v0.1.0` release/tag exists yet.

## Purpose

SMO defines a deliberately small reusable boundary between authoritative machine-interpretable semantics and implementation-facing projections of those semantics.

The v0.1 architectural invariant is:

> **Projection or derivation does not transfer semantic authority.**

An implementation projection may preserve, transform, introduce, or omit structures for its target while remaining non-authoritative for the source semantics it projects.

## v0.1 vocabulary

Version 0.1 owns exactly two classes and no SMO-specific relation.

### `smo:SemanticModel`

> A formal representation that gives knowledge explicit machine-interpretable meaning through concepts, relationships, constraints, axioms, or equivalent semantic structures.

### `smo:ImplementationProjection`

> A non-authoritative implementation-facing projection derived from selected semantics of a Semantic Model, preserving explicit semantic identity and relationships according to a declared preservation, transformation, introduction, and omission policy while allowing target-specific implementation concerns.

For derivation, source, conformance, publication, and provenance evidence, reuse established vocabularies such as PROV-O, Dublin Core Terms, DCAT, and OWL rather than minting parallel SMO relations.

## Namespace and publication state

```text
machine state       activation-requested
term namespace      https://w3id.org/smo#
ontology IRI        https://w3id.org/smo
version IRI         https://w3id.org/smo/0.1.0
semantic version    0.1.0
W3ID request        perma-id/w3id.org#6538 — open
current route       not yet claimed active
immutable release   not yet created
immutable route     deferred
```

The semantic identifiers are governed now, but publication activation is intentionally treated as a separate observable state. Until upstream W3ID merge and external resolver verification are complete, the current route remains inactive in the publication contract.

The immutable `https://w3id.org/smo/0.1.0` route is not part of PR #6538. It remains deferred until an immutable `smo-v0.1.0` backend exists.

GitHub URLs in the publication configuration are backend locations only and are never SMO semantic identities.

## Repository structure

```text
README.md
LICENSE
CONTRIBUTING.md
model/
  smo.ttl
  publication-contract.json
  verify-model.py
publication/
  backend-targets.json
  w3id/
    .htaccess
    README.md
docs/
  namespace-publication-versioning.md
.github/
  workflows/
    verify.yml
```

The earlier exploratory meta-ontology surface has intentionally been removed from the v0.1 baseline. Runtime context, agent contracts, model kinds, mappings, transformations, representations, authority vocabulary, and similar concepts require separate evidence before becoming SMO-owned terms.

## Verification

Install the validator dependency and run the executable acceptance contract:

```bash
python -m pip install rdflib
python model/verify-model.py
```

CI runs the same verification for pull requests and pushes to `main`.

The verifier currently proves the intermediate publication state:

1. the ontology still owns exactly `SemanticModel` and `ImplementationProjection` and no SMO properties;
2. W3ID PR #6538 is recorded as submitted;
3. the current route is not claimed active before external verification;
4. the immutable route remains deferred until `smo-v0.1.0` exists.

## Publication and versioning

See [`docs/namespace-publication-versioning.md`](docs/namespace-publication-versioning.md) for the machine-aligned namespace, backend, staging, versioning, and acceptance contract.

The next publication transition is triggered by upstream merge of W3ID PR #6538. Only after external HTML/Turtle verification should the current namespace be marked active and the governed `smo-v0.1.0` release/version-route sequence proceed.

Downstream ESKA/Pizza alignment remains staged under SMO #11 until the live current namespace and immutable v0.1.0 publication evidence exist.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
