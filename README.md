# Semantic Modeling Ontology

An ontology for describing semantic models, their elements, constraints, mappings, projections, provenance, and operational artifacts.

> **Status:** Exploratory. The vocabulary and its semantics are expected to evolve substantially before a first stable release.

## Core idea

Semantic models should not only describe domains. They should also be machine-readable artifacts that describe their own kind, structure, language, derivation, constraints, representations, and operational projections.

The Semantic Modeling Ontology provides a small semantic foundation for describing:

- ontologies and semantic models;
- model elements and modeling languages;
- semantic views, projections, and specializations;
- constraints, mappings, and transformations;
- generated and operational artifacts;
- runtime contexts and agent contracts;
- the Semantic Modeling Ontology itself.

## Conceptual flow

```text
Capability
        ↓
Capability Ontology
        ↓
Capability Semantic Model
        ↓
Domain Models
        ↓
APIs / UI / Rules / Data / Agent Contracts
        ↓
Runtime Context
```

The ontology describes the relationships between these artifacts without attempting to replace the specialized languages used to implement them.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── docs/
│   └── architecture.md
├── ontology/
│   └── semantic-modeling.ttl
├── shapes/
│   └── semantic-modeling-shapes.ttl
└── examples/
    └── self-description.ttl
```

## Architecture

The design rationale, scope, competency questions, core concepts, and open questions are maintained in [`docs/architecture.md`](docs/architecture.md).

## Initial milestone

The first milestone is **v0.1 — Models, projections, and artifacts**. It should demonstrate that:

1. the ontology can describe itself as a semantic model;
2. SHACL can validate that self-description;
3. one model can be represented as a projection or specialization of another;
4. operational artifacts can be traced to the models from which they were derived;
5. SPARQL can inspect the resulting model graph.

## License

Licensed under the MIT License. See [`LICENSE`](LICENSE).
