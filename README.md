# Semantic Modeling Ontology (SMO)

A small, standards-aligned ontology for authoritative semantic models and their non-authoritative implementation projections.

> **Status:** SMO publication is **version-active**. The current namespace `https://w3id.org/smo` and immutable version IRI `https://w3id.org/smo/0.1.0` are active and live-verified. The governed immutable repository release [`smo-v0.1.0`](https://github.com/GerhardBalz/semantic-modeling-ontology/releases/tag/smo-v0.1.0) remains the backend for the versioned route.

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
machine state         version-active
term namespace        https://w3id.org/smo#
ontology IRI          https://w3id.org/smo
version IRI           https://w3id.org/smo/0.1.0
semantic version      0.1.0
W3ID current route    active and live-verified
immutable release     smo-v0.1.0 — published
release commit        e6ab3f8cf14bafae466a0150ad356547f164bdab
immutable backend     verified
immutable W3ID route  active and live-verified
```

Current-route activation evidence is recorded in `model/publication-contract.json`: upstream W3ID PR #6538, merge commit `42367a77c52b60dab4cdf55327fca023e78a61a4`, and live verification run `31627245287`.

Release evidence is also recorded there: tag `smo-v0.1.0`, governed release commit `e6ab3f8cf14bafae466a0150ad356547f164bdab`, publisher run `31633781524`, and the verified immutable Turtle backend under the tag.

Immutable version-route evidence is recorded as upstream W3ID PR #6541, merge commit `84d541d959006ea6df14014e880020223c3c059b`, verifier commit `e9422be4aa01e8889bb11b6e4dc38348c4e55a98`, and successful current+immutable live verification run `31642224022`.

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
  releases/
    smo-v0.1.0.json
  w3id/
    .htaccess
    README.md
docs/
  namespace-publication-versioning.md
  releases/
    smo-v0.1.0.md
.github/
  workflows/
    verify.yml
    verify-live-w3id.yml
    publish-smo-v0.1.0.yml
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
2. W3ID PR #6538 and current-route merge/live evidence are recorded;
3. the governed `smo-v0.1.0` release and exact release commit are recorded;
4. the immutable tagged backend exists and is recorded as verified;
5. W3ID PR #6541 and immutable-route merge/live evidence are recorded;
6. both current and immutable routes are active only with successful live verification evidence.

The live resolver verifier is `publication/verify-live-w3id.py`. It follows only internal `w3id.org` canonicalization hops, verifies terminal governed redirect targets, and fetches RDF backends separately for semantic evidence.

## Publication and versioning

See [`docs/namespace-publication-versioning.md`](docs/namespace-publication-versioning.md) for the machine-aligned namespace, backend, state-machine, versioning, and acceptance contract.

The publication gate for durable downstream references is now satisfied. The next governed activity is SMO #11: evaluate downstream SMO alignment in ESKA and Pizza without modifying immutable `smo-v0.1.0`, immutable `eska-v0.1.0`, or historical Pizza semantics merely for symmetry.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
