# Semantic Modeling Ontology (SMO)

A small, standards-aligned ontology for authoritative semantic models and their non-authoritative implementation projections.

> **Status:** v0.1 bootstrap, pre-activation. The prepared namespace `https://w3id.org/smo#` is not yet claimed to be live, no W3ID request has been submitted by this baseline, and no `smo-v0.1.0` release/tag is created here.

## Purpose

SMO defines a deliberately small reusable boundary between authoritative machine-interpretable semantics and implementation-facing projections of those semantics.

The v0.1 architectural invariant is:

> **Projection or derivation does not transfer semantic authority.**

An implementation projection may preserve, transform, introduce, or omit structures for its target while remaining non-authoritative for the source semantics it projects.

## v0.1 vocabulary

Version 0.1 owns exactly two classes and no SMO-specific relation:

### `smo:SemanticModel`

> A formal representation that gives knowledge explicit machine-interpretable meaning through concepts, relationships, constraints, axioms, or equivalent semantic structures.

### `smo:ImplementationProjection`

> A non-authoritative implementation-facing projection derived from selected semantics of a Semantic Model, preserving explicit semantic identity and relationships according to a declared preservation, transformation, introduction, and omission policy while allowing target-specific implementation concerns.

For derivation, source, conformance, publication, and provenance evidence, reuse established vocabularies such as PROV-O, Dublin Core Terms, DCAT, and OWL rather than minting parallel SMO relations.

## Prepared namespace

```text
term namespace  https://w3id.org/smo#
ontology IRI    https://w3id.org/smo
version IRI     https://w3id.org/smo/0.1.0
version         0.1.0
```

These are prepared semantic identifiers. Until W3ID activation is completed and externally verified, the publication status remains **pre-activation**.

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

## Publication and versioning

See [`docs/namespace-publication-versioning.md`](docs/namespace-publication-versioning.md) for the machine-aligned namespace, backend, staging, versioning, and acceptance contract.

The prepared W3ID payload is intentionally inactive. Do not request `w3id.org/smo`, create `smo-v0.1.0`, modify ESKA `SemanticModel`, or align Pizza as part of this bootstrap PR.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
