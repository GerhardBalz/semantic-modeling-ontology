# SMO W3ID publication payload

This directory contains the redirect configuration prepared for the permanent Semantic Modeling Ontology namespace:

```text
https://w3id.org/smo
```

## Maintainer

- Gerhard Balz — GitHub [`@GerhardBalz`](https://github.com/GerhardBalz)

## Canonical project

- Repository: `GerhardBalz/semantic-modeling-ontology`
- Prepared term namespace: `https://w3id.org/smo#`
- Prepared ontology IRI: `https://w3id.org/smo`

## Activation scope

The initial W3ID request activates only current governed publication routes:

- browser requests for `https://w3id.org/smo` → project repository;
- Turtle requests for `https://w3id.org/smo` → `main/model/smo.ttl`;
- `https://w3id.org/smo/docs` → namespace/publication documentation;
- `https://w3id.org/smo/dist/smo.ttl` → current authoritative Turtle.

The prepared ontology `owl:versionIRI` is `https://w3id.org/smo/0.1.0`, but **no immutable version redirect is submitted in this activation payload**. That route will be added only after the governed `smo-v0.1.0` release tag exists, so a permanent version identifier can never point at a mutable or nonexistent backend.

GitHub and raw GitHub URLs are replaceable publication backends, not SMO semantic identities.
