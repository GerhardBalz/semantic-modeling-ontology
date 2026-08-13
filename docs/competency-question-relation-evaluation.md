# Competency-question relation evaluation

## Decision

Do **not** add a new SMO competency-question property from the current evidence.

The cross-example need is real, but an established vocabulary already covers the core textual competency-question use case:

```text
https://w3id.org/mod#competencyQuestion
```

Current MOD defines `mod:competencyQuestion` for a `mod:SemanticArtefact` with a string value. MOD also defines:

```text
https://w3id.org/mod#designedForTask
```

from a semantic artefact to a semantic-artefact task.

SMO should therefore remain small and standards-aligned rather than minting `smo:answersQuestion` or equivalent vocabulary now.

## Evidence that triggered the evaluation

### Semantic Modeling Pizza

The Pizza Menu Semantic Model independently records four competency questions using repository-local experimental `smp:answersQuestion`.

Semantic Modeling Pizza #6 / PR #7 deliberately kept that relation local while correcting all governed SMO usage.

### Semantic Modeling Wine/Food

Wine/Food #3 / PR #4 independently introduced a machine-expressible `smwf:answersQuestion` relation and used it in a deterministic recommendation example.

This establishes genuine cross-domain recurrence of the semantic-model → competency-question need.

## Standards review

### DCTERMS

`dcterms:description` is intentionally generic: it gives an account of a resource. `dcterms:relation` and its subproperties are likewise generic related-resource relationships.

They are useful for general metadata but do not name the ontology-engineering concept of a competency question precisely.

Reference:

- https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

### MOD — Metadata for Ontology Description and Publication

Current MOD provides the direct term:

```text
mod:competencyQuestion
IRI: https://w3id.org/mod#competencyQuestion
Domain: mod:SemanticArtefact
Range: string
```

It also provides:

```text
mod:designedForTask
IRI: https://w3id.org/mod#designedForTask
Domain: mod:SemanticArtefact
Range: mod:SemanticArtefactTask
```

References:

- https://fair-impact.github.io/MOD/index-en.html
- https://w3id.org/mod

The earlier MOD specification already defined `competencyQuestion` for ontology design-time questions; the current W3ID-based MOD broadens its domain to semantic artefacts.

## Compatibility with SMO

SMO defines `smo:SemanticModel` as:

> A formal representation that gives knowledge explicit machine-interpretable meaning through concepts, relationships, constraints, axioms, or equivalent semantic structures.

This is compatible in intent with treating many SMO semantic models as semantic artefacts, but SMO should **not** assert a class equivalence or subclass relation to `mod:SemanticArtefact` merely to reuse one metadata property. Such an alignment would be a broader modeling decision requiring its own evidence.

Downstream data may intentionally use both vocabularies without importing MOD into SMO itself.

## Literal question vs first-class question resource

The two reference examples currently differ in representation:

- Pizza records competency questions as literals;
- Wine/Food introduces an identified competency-question resource.

`mod:competencyQuestion` directly covers the literal case.

The current evidence does **not** yet establish a reusable need for SMO to model competency questions as first-class resources. A project that needs question identity, lifecycle, provenance, type, validation status, mappings, or decomposition can use a local/requirements vocabulary and may additionally expose the textual question through `mod:competencyQuestion`.

Do not create a resource-valued SMO property merely to preserve the current Wine/Food local shape.

## Recommended convention

For a semantic model with textual competency questions:

```turtle
@prefix smo: <https://w3id.org/smo#> .
@prefix mod: <https://w3id.org/mod#> .

ex:MyModel
    a smo:SemanticModel ;
    mod:competencyQuestion "Which candidate wines match this meal course and preference profile?"@en .
```

Where a separately identified task is the relevant purpose abstraction, evaluate `mod:designedForTask` rather than overloading competency questions.

No `owl:imports` from SMO to MOD is required for downstream consumers to reuse the MOD property IRI.

## Negative boundaries

This decision does not justify adding to SMO:

- `answersQuestion`;
- a `CompetencyQuestion` class;
- exclusion/inclusion relations;
- runtime-context concepts;
- operation signatures;
- recommendation-evidence structures;
- generic representation or provenance relations.

Those remain local, established-vocabulary, or ESKA concerns according to the SKE evidence review.

## Migration implication for reference examples

A later repository-local cleanup may:

- replace Pizza's literal `smp:answersQuestion` assertions with `mod:competencyQuestion`;
- expose Wine/Food's competency-question text with `mod:competencyQuestion`, retaining a local first-class question resource only if resource identity is demonstrably useful.

Those are downstream adoption tasks, not SMO vocabulary changes.

## Publication/versioning impact

None.

`model/smo.ttl`, governed SMO v0.1.0, its immutable tag, and its W3ID publication remain unchanged.

## Re-evaluation trigger

Revisit a resource-valued reusable relation only if multiple independent domains require first-class competency-question resources and established vocabularies cannot express the needed semantics without loss.

Related: SMO #22, SKE #25/#27, Semantic Modeling Pizza #6/PR #7, Semantic Modeling Wine/Food #3/PR #4.