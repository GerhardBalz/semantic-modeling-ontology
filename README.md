# Semantic Modeling Ontology (SMO)

A small, standards-aligned ontology for authoritative semantic models and their non-authoritative implementation projections.

> **Status:** current W3ID publication is **active**. `https://w3id.org/smo` was activated through [`perma-id/w3id.org#6538`](https://github.com/perma-id/w3id.org/pull/6538) and verified live by GitHub Actions. The governed `smo-v0.1.0` release/tag and immutable `0.1.0` route are still pending.

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
machine state       current-active
term namespace      https://w3id.org/smo#
ontology IRI        https://w3id.org/smo
version IRI         https://w3id.org/smo/0.1.0
semantic version    0.1.0
W3ID request        perma-id/w3id.org#6538 — merged
current route       active and live-verified
immutable release   not yet created
immutable route     deferred
```

Activation evidence is recorded in `model/publication-contract.json`: upstream W3ID merge commit `42367a77c52b60dab4cdf55327fca023e78a61a4` and live verification workflow run `31627245287`.

The immutable `https://w3id.org/smo/0.1.0` route remains deferred until an immutable `smo-v0.1.0` backend exists.

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
  verify-live-w3id.py
  w3id/
    .htaccess
    README.md
docs/
  namespace-publication-versioning.md
.github/
  workflows/
    verify.yml
    verify-live-w3id.yml
```

The earlier exploratory meta-ontology surface has intentionally been removed from the v0.1 baseline. Runtime context, agent contracts, model kinds, mappings, transformations, representations, authority vocabulary, and similar concepts require separate evidence before becoming SMO-owned terms.

## Verification

Install the validator dependency and run the executable acceptance contract:

```bash
python -m pip install rdflib
python model/verify-model.py
```

The governed verifier proves that:

1. the ontology still owns exactly `SemanticModel` and `ImplementationProjection` and no SMO properties;
2. W3ID PR #6538 is recorded as merged;
3. the current route is recorded active only with live verification evidence;
4. the immutable route remains deferred until `smo-v0.1.0` exists.

The live resolver verifier is `publication/verify-live-w3id.py` and is executable through GitHub Actions.

## Publication and versioning

See [`docs/namespace-publication-versioning.md`](docs/namespace-publication-versioning.md) for the machine-aligned namespace, backend, staging, versioning, and acceptance contract.

The next governed transition is creation of the immutable `smo-v0.1.0` release from the active publication baseline. Only after that immutable backend exists should `https://w3id.org/smo/0.1.0` be activated.

Downstream ESKA/Pizza alignment remains staged under SMO #11 until both current and immutable publication evidence exist.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
