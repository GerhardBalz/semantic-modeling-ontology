# Architecture

## 1. Purpose

The Semantic Modeling Ontology (SMO) defines the concepts and relationships required to describe semantic models as machine-readable artifacts.

It is intended to describe not only what a model contains, but also:

- what kind of model it is;
- which modeling languages it uses;
- how it relates to other models;
- which constraints and mappings apply to it;
- which views, projections, or specializations are derived from it;
- which operational artifacts are generated from it;
- which runtime context makes a model or artifact relevant;
- how the Semantic Modeling Ontology describes itself.

The ontology is a semantic foundation for model management, introspection, validation, traceability, and future artifact generation.

## 2. Motivation

Semantic models are often stored as files whose role and relationships are known mainly through conventions, repository structures, or human documentation.

For example, a project may contain:

- an OWL ontology;
- SHACL shapes;
- a domain model;
- database mappings;
- an OpenAPI description;
- an agent contract;
- generated documentation.

The individual artifacts may be machine-readable, while the relationships between them remain implicit.

SMO makes these relationships explicit. A model can state which kind of model it is, which languages it uses, which source model it projects, and which artifacts were derived from it.

## 3. Core idea

The central idea is that semantic models can themselves be described semantically.

```text
A semantic model describes a domain.

The Semantic Modeling Ontology describes semantic models.

The Semantic Modeling Ontology is itself a semantic model.
```

This provides reflection and self-description: SMO uses its own concepts to state that it is a model, identify its model kind and modeling languages, and describe its elements and representations.

For example:

```turtle
@prefix smo: <https://github.com/GerhardBalz/semantic-modeling-ontology#> .

<https://github.com/GerhardBalz/semantic-modeling-ontology>
    a smo:Model ;
    smo:hasModelKind smo:OntologyModelKind ;
    smo:usesLanguage smo:OWL, smo:SHACL .
```

The ontology defines what a `smo:Model` is and is itself described as one of those models. Because the self-description is model data, the same queries, validation rules, documentation generators, and other tools used for external semantic models can also be applied to SMO.

This does not yet make SMO self-generating or self-hosting. Those are possible later stages in which SMO drives the generation of tooling that can process SMO itself.

## 4. Architectural context

SMO is positioned above domain-specific semantic models and below operational tooling.

```text
Semantic modeling foundations
RDF / RDFS / OWL / SHACL / SKOS / PROV-O / SPARQL
        ↓
Semantic Modeling Ontology
        ↓ describes
Capability Ontologies / Semantic Models / Domain Models
        ↓ projects and realizes
Mappings / Constraints / Views / Agent Contracts
        ↓ operationalizes
APIs / UI / Rules / Data / AI / Runtime Context
```

SMO does not replace the languages in the foundation layer. It provides vocabulary for describing how models and artifacts use those languages and relate to one another.

## 5. Modeling levels

A useful conceptual separation is:

```text
M3 — Semantic modeling foundations
     RDF, RDFS, OWL, SHACL, SKOS, PROV-O

M2 — Semantic Modeling Ontology
     Model, Model Element, Model Kind, Projection,
     Constraint, Mapping, Artifact, Runtime Context

M1 — Concrete models
     Capability Ontology, Capability Semantic Model,
     Pricing Domain Model, Pricing Agent Contract

M0 — Runtime entities and facts
     Customer 4711, Pricing Agreement 823,
     Fee Condition 17, Pricing Simulation 905
```

RDF permits resources from these levels to coexist in one graph. SMO therefore relies on explicit model kinds and relationships rather than assuming that graph separation alone communicates modeling level.

## 6. Semantic technology responsibilities

SMO uses several complementary standards.

| Technology | Responsibility |
|---|---|
| RDF | Common graph representation and global identity |
| RDFS | Basic classes, properties, labels, domains, and ranges |
| OWL | Formal meaning, logical relationships, and inference |
| SHACL | Structural constraints and validation |
| SKOS | Controlled concepts, classifications, and terminology |
| PROV-O | Derivation, generation, responsibility, and provenance |
| SPARQL | Introspection, queries, transformations, and reports |
| JSON Schema / OpenAPI / MCP | Operational projections for applications and agents |

The ontology should reuse established vocabularies rather than redefine their concepts.

## 7. Initial conceptual model

### 7.1 Core classes

The initial vocabulary contains the following classes:

- **Model** — a coherent representation created for a purpose;
- **ModelElement** — an identifiable element contained in or referenced by a model;
- **ModelKind** — a classification describing the role of a model;
- **ModelingLanguage** — a language used to express a model;
- **ModelRepresentation** — a concrete representation or serialization of a model;
- **SemanticView** — a task-, audience-, or context-specific model view;
- **Constraint** — a condition that a model or artifact is expected to satisfy;
- **Mapping** — a correspondence between model elements or representations;
- **Transformation** — an activity that derives one model or artifact from another;
- **Artifact** — a concrete deliverable related to a model;
- **RuntimeContext** — the circumstances in which a model, view, or artifact applies;
- **AgentContract** — an operational semantic contract exposed to an AI agent.

### 7.2 Core relationships

The initial vocabulary contains relationships for:

- containing model elements;
- assigning a model kind;
- declaring modeling languages;
- linking concrete representations;
- importing another model;
- deriving one entity from another;
- projecting or specializing another model;
- realizing a model in another representation;
- associating constraints and mappings;
- generating operational artifacts;
- linking artifacts back to their source models;
- applying a model or artifact in a runtime context.

## 8. Model kinds

The first version distinguishes several model kinds:

- **Ontology Model** — defines the meaning of concepts and relationships;
- **Semantic Model** — provides a canonical semantic representation for people and systems;
- **Domain Model** — represents a domain or bounded context for a particular purpose;
- **Constraint Model** — defines structural or semantic validity conditions;
- **Agent Contract Model** — exposes a task-oriented operational projection to an agent.

These kinds are initially represented as controlled concepts. The classification is expected to evolve as concrete use cases clarify the boundaries.

## 9. Model derivation chain

A primary use case is to describe a traceable chain from enduring meaning to operational artifacts.

```text
Capability
        ↓
Capability Ontology
        ↓ projected as
Capability Semantic Model
        ↓ specialized as
Domain Model
        ↓ operationalized as
API / UI / Rules / Data / Agent Contract
        ↓ activated in
Runtime Context
```

Here, **Capability** is intentionally broader than **Business Capability**. A capability may be a business, product, system, platform, organizational, or agent capability.

An operational artifact is not identical to the ontology from which it was derived. It is a governed, purpose-specific projection or realization.

For example:

```text
Customer Ontology
    ├── search_customer agent contract
    ├── assess_customer_eligibility agent contract
    ├── Customer API
    └── Customer database mapping
```

Each artifact exposes only the semantics required for its purpose.

## 10. Self-description

SMO should be able to describe itself as a model.

The self-description should state at least:

- that SMO is an ontology and a model;
- that it has the model kind Ontology Model;
- that it uses RDF, RDFS, OWL, SHACL, and SKOS;
- which representations belong to it;
- which core model elements it defines;
- which version is being described.

This is reflection: the vocabulary is used to describe the vocabulary artifact itself.

Self-reference alone does not make the ontology executable or self-aware. It becomes operationally useful when validators, queries, generators, or editors consume the description.

## 11. Self-validation

SHACL shapes define minimum structural expectations for SMO models.

The first shapes require that every `Model` has:

- a title;
- at least one model kind;
- at least one modeling language.

Additional shapes validate projections, generated artifacts, and model elements.

Because the Semantic Modeling Ontology is itself described as a `Model`, its self-description is subject to the same validation rules.

```text
The ontology defines what a Model is.
The ontology is described as a Model.
The ontology must therefore satisfy the Model constraints.
```

## 12. Self-generation and self-hosting

The following concepts must remain distinct:

### Self-describing

The model contains machine-readable statements about its own kind, elements, languages, versions, and relationships.

### Self-validating

The model is checked against constraints expressed in a machine-readable validation language such as SHACL.

### Self-generating

The model drives generation of documentation, schemas, diagrams, code, tests, or operational contracts.

### Self-hosting

Tooling generated from the model can process and regenerate the model and its own tooling definitions.

Version 0.1 targets self-description and self-validation. Self-generation and self-hosting are future concerns.

## 13. Competency questions

The ontology should make it possible to answer questions such as:

1. What kind of model is this?
2. Which modeling languages does it use?
3. Which concepts or model elements does it define?
4. Which model is this model derived from?
5. Is it a projection, specialization, or realization of another model?
6. Which constraints apply to it?
7. Which mappings connect it to databases, APIs, events, or knowledge graphs?
8. Which operational artifacts were generated from it?
9. Which model version generated a particular artifact?
10. Which runtime context activates a semantic view or agent contract?
11. Who created, owns, maintains, or approved the model?
12. Can the ontology describe and validate its own representation?

These questions should drive vocabulary additions. New concepts should not be introduced merely to mirror another metamodel comprehensively.

## 14. Design principles

### 14.1 Small semantic core

Start with the minimum concepts required to describe models, derivations, and artifacts. Extend the ontology through demonstrated use cases.

### 14.2 Reuse before reinvention

Use Dublin Core Terms for descriptive metadata, SKOS for controlled concepts, PROV-O for provenance, OWL for semantics, and SHACL for validation.

### 14.3 Meaning before serialization

A model is distinct from a particular Turtle, RDF/XML, JSON-LD, diagram, or document representation.

### 14.4 Projection rather than duplication

Domain models, APIs, and agent contracts should be represented as governed projections or realizations of semantic foundations rather than disconnected copies.

### 14.5 Traceability by design

Derived models and artifacts should retain machine-readable links to their sources, transformations, and versions.

### 14.6 Explicit runtime context

Meaning may be enduring, while relevance is contextual. Runtime context should identify which model views, facts, policies, and tools matter for a task.

### 14.7 Avoid premature metamodel completeness

SMO is not intended to reproduce all of UML, MOF, ArchiMate, OWL, SHACL, OpenAPI, or MCP. It describes how their artifacts participate in a semantic modeling lifecycle.

## 15. Scope of v0.1

Version 0.1 focuses on:

- models and model elements;
- model kinds and modeling languages;
- views, projections, specializations, and realizations;
- constraints and mappings;
- artifacts and derivation traceability;
- runtime context;
- self-description;
- basic SHACL validation.

## 16. Non-goals for v0.1

The following are explicitly outside the first version:

- a complete UML or MOF metamodel;
- a complete enterprise architecture metamodel;
- detailed OWL language metamodeling;
- graphical notation and layout;
- executable agent behavior semantics;
- database-specific mapping languages;
- a complete API modeling language;
- general process modeling;
- unrestricted higher-order logic;
- production-ready code generation.

## 17. Repository structure

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

The architecture remains in one coherent document until size, ownership, or change frequency justifies extracting sections into separate documents.

## 18. Open questions

The initial implementation intentionally leaves several questions open:

1. Should `AgentContract` be primarily a `Model`, an `Artifact`, or both?
2. Should model kinds remain SKOS concepts or become OWL classes?
3. How should model versions and immutable version IRIs be represented?
4. Should mappings be modeled as declarative artifacts, transformation activities, or both?
5. How should named graphs or datasets delimit models and runtime facts?
6. How much formal domain and range information should be declared without causing unintended OWL inferences?
7. Which namespace should become the durable public ontology IRI?
8. How should external specifications such as OpenAPI and MCP be linked without reproducing their internal metamodels?
9. Which parts of the model should eventually generate SHACL, JSON Schema, OpenAPI, or MCP artifacts?

## 19. Initial milestone

The first milestone is **v0.1 — Models, projections, and artifacts**.

Acceptance criteria:

1. SMO can describe itself as a model.
2. SHACL can validate the self-description.
3. A capability ontology can be represented.
4. A capability semantic model can be declared as its projection.
5. A domain model can specialize the semantic model.
6. An agent contract can be linked as an operational artifact.
7. A SPARQL query can trace the complete derivation chain.

## 20. Evolution approach

The ontology should evolve through concrete examples rather than abstract completeness.

A likely sequence is:

```text
v0.1  Models, projections, and artifacts
v0.2  Provenance, versions, and governance
v0.3  Mappings and transformations
v0.4  Operational contracts and runtime context
v0.5  Generation and introspection tooling
```

These version labels are directional and may change as the model is tested against real projects.
