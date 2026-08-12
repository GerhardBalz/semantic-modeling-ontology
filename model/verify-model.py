#!/usr/bin/env python3
"""Verify the SMO v0.1 ontology and pre-activation publication contract."""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "model/publication-contract.json"
BACKENDS_PATH = ROOT / "publication/backend-targets.json"
W3ID_PATH = ROOT / "publication/w3id/.htaccess"
README_PATH = ROOT / "README.md"
DOC_PATH = ROOT / "docs/namespace-publication-versioning.md"

EXPECTED_NAMESPACE = "https://w3id.org/smo#"
EXPECTED_ONTOLOGY_IRI = "https://w3id.org/smo"
EXPECTED_VERSION_IRI = "https://w3id.org/smo/0.1.0"
EXPECTED_VERSION = "0.1.0"
EXPECTED_CLASSES = {"SemanticModel", "ImplementationProjection"}
EXPECTED_DEFINITIONS = {
    "SemanticModel": (
        "A formal representation that gives knowledge explicit machine-interpretable meaning "
        "through concepts, relationships, constraints, axioms, or equivalent semantic structures."
    ),
    "ImplementationProjection": (
        "A non-authoritative implementation-facing projection derived from selected semantics of a "
        "Semantic Model, preserving explicit semantic identity and relationships according to a "
        "declared preservation, transformation, introduction, and omission policy while allowing "
        "target-specific implementation concerns."
    ),
}
FORBIDDEN_ESKA_FRAGMENTS = {
    "capability",
    "execution",
    "result",
    "verification",
    "service",
    "agent",
    "deployment",
}
GITHUB_IDENTITY_PREFIX = "https://github.com/GerhardBalz/semantic-modeling-ontology"
RAW_BACKEND_PREFIX = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def local_name(uri: URIRef) -> str:
    text = str(uri)
    require(text.startswith(EXPECTED_NAMESPACE), f"not an SMO term IRI: {text}")
    return text[len(EXPECTED_NAMESPACE) :]


def main() -> None:
    contract = read_json(CONTRACT_PATH)
    backends = read_json(BACKENDS_PATH)
    ontology_path = ROOT / contract["ontology"]["path"]

    # 1. Parse the ontology as Turtle.
    graph = Graph()
    graph.parse(ontology_path, format="turtle")

    # 2. Verify ontology identity and semantic version contract.
    require(contract["contractVersion"] == "1.0", "unexpected publication contract version")
    require(contract["status"] == "pre-activation", "SMO bootstrap must remain pre-activation")
    require(contract["repository"] == "GerhardBalz/semantic-modeling-ontology", "repository mismatch")
    require(contract["termNamespace"]["current"] == EXPECTED_NAMESPACE, "term namespace mismatch")
    require(contract["termNamespace"]["activationStatus"] == "not-active", "namespace must not be active")
    require(contract["termNamespace"]["resolver"] == EXPECTED_ONTOLOGY_IRI, "resolver mismatch")

    ontology_iri = URIRef(EXPECTED_ONTOLOGY_IRI)
    version_iri = URIRef(EXPECTED_VERSION_IRI)
    require((ontology_iri, RDF.type, OWL.Ontology) in graph, "expected ontology IRI is not declared")
    require(
        graph.value(ontology_iri, OWL.versionIRI) == version_iri,
        "ontology owl:versionIRI does not match publication contract",
    )
    require(
        graph.value(ontology_iri, OWL.versionInfo) == Literal(EXPECTED_VERSION),
        "ontology owl:versionInfo does not match publication contract",
    )
    require(contract["ontology"]["ontologyIri"] == EXPECTED_ONTOLOGY_IRI, "contract ontology IRI mismatch")
    require(contract["ontology"]["versionIri"] == EXPECTED_VERSION_IRI, "contract version IRI mismatch")
    require(contract["ontology"]["version"] == EXPECTED_VERSION, "contract semantic version mismatch")

    # 3. Verify the complete SMO-owned term inventory.
    owned_uris: set[URIRef] = set()
    for subject, predicate, obj in graph:
        for value in (subject, predicate, obj):
            if isinstance(value, URIRef) and str(value).startswith(EXPECTED_NAMESPACE):
                owned_uris.add(value)
    owned_locals = {local_name(uri) for uri in owned_uris}
    require(owned_locals == EXPECTED_CLASSES, f"unexpected SMO-owned terms: {sorted(owned_locals)}")

    declared_classes = {
        local_name(subject)
        for subject in graph.subjects(RDF.type, OWL.Class)
        if isinstance(subject, URIRef) and str(subject).startswith(EXPECTED_NAMESPACE)
    }
    require(declared_classes == EXPECTED_CLASSES, f"expected exactly two SMO classes, found {sorted(declared_classes)}")
    require(contract["ownedTerms"]["classes"] == ["SemanticModel", "ImplementationProjection"], "class inventory contract changed")
    require(contract["ownedTerms"]["objectProperties"] == [], "v0.1 must not own object properties")
    require(contract["ownedTerms"]["datatypeProperties"] == [], "v0.1 must not own datatype properties")

    for property_type in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
        owned_properties = [
            subject
            for subject in graph.subjects(RDF.type, property_type)
            if isinstance(subject, URIRef) and str(subject).startswith(EXPECTED_NAMESPACE)
        ]
        require(not owned_properties, f"v0.1 must not mint SMO properties: {owned_properties}")

    # 4. Verify definitions and language tags.
    for name, expected_definition in EXPECTED_DEFINITIONS.items():
        term = URIRef(EXPECTED_NAMESPACE + name)
        definitions = list(graph.objects(term, RDFS.comment))
        require(definitions == [Literal(expected_definition, lang="en")], f"{name}: definition or language tag mismatch")
        labels = list(graph.objects(term, RDFS.label))
        require(len(labels) == 1 and isinstance(labels[0], Literal) and labels[0].language == "en", f"{name}: English label required")

    # 5. Make the ESKA boundary explicit even though the exact term inventory already constrains it.
    for name in owned_locals:
        lowered = name.lower()
        require(
            not any(fragment in lowered for fragment in FORBIDDEN_ESKA_FRAGMENTS),
            f"ESKA-specific concept leaked into SMO: {name}",
        )

    # 6. GitHub is allowed as a transport backend, never as semantic identity.
    github_semantic_uris = {
        str(value)
        for triple in graph
        for value in triple
        if isinstance(value, URIRef) and str(value).startswith(GITHUB_IDENTITY_PREFIX)
    }
    require(not github_semantic_uris, f"GitHub URL used as semantic identity: {sorted(github_semantic_uris)}")

    # 7. Verify prepared backend targets are governed and explicitly inactive.
    require(backends["contractVersion"] == contract["contractVersion"], "backend contract version mismatch")
    require(backends["status"] == "pre-activation", "backend targets must remain pre-activation")
    require(backends["repository"] == contract["repository"], "backend repository mismatch")
    require(backends["branch"] == "main", "current publication backend must target main")
    routes = {entry["kind"]: entry for entry in backends["routes"]}
    require(set(routes) == {"current", "version"}, "expected current and version backend routes")
    require(routes["current"]["route"] == EXPECTED_ONTOLOGY_IRI, "current W3ID route mismatch")
    require(routes["version"]["route"] == EXPECTED_VERSION_IRI, "version W3ID route mismatch")
    require(routes["version"].get("requiresTag") == "smo-v0.1.0", "immutable target must require smo-v0.1.0")
    for entry in routes.values():
        require(entry["active"] is False, f"prepared route must not claim activation: {entry['route']}")
        require(entry["target"].startswith(RAW_BACKEND_PREFIX), f"backend is outside governed repository: {entry['target']}")

    require(contract["publication"]["w3idRequested"] is False, "bootstrap must not claim a W3ID request")
    require(contract["publication"]["w3idActive"] is False, "bootstrap must not claim W3ID activation")
    require(contract["releaseVersioning"]["releaseCreated"] is False, "bootstrap must not claim a release/tag")

    htaccess = W3ID_PATH.read_text(encoding="utf-8")
    require("PRE-ACTIVATION" in htaccess, "W3ID payload must be visibly pre-activation")
    for entry in routes.values():
        require(entry["target"] in htaccess, f"W3ID payload missing backend target: {entry['target']}")

    # 8. Verify human-readable publication documentation matches the machine contract.
    required_documentation_tokens = (
        EXPECTED_NAMESPACE,
        EXPECTED_ONTOLOGY_IRI,
        EXPECTED_VERSION_IRI,
        EXPECTED_VERSION,
        "pre-activation",
        "smo-v0.1.0",
    )
    for path in (README_PATH, DOC_PATH):
        text = path.read_text(encoding="utf-8")
        for token in required_documentation_tokens:
            require(token in text, f"{path.relative_to(ROOT)} missing publication-contract token: {token}")

    print("SUCCESS: SMO v0.1 bootstrap contract is machine-verifiable.")
    print(f"Term namespace:          {EXPECTED_NAMESPACE}")
    print(f"Ontology IRI:            {EXPECTED_ONTOLOGY_IRI}")
    print(f"Version IRI:             {EXPECTED_VERSION_IRI}")
    print(f"Declared SMO classes:    {len(declared_classes)}")
    print("SMO-owned properties:   0")
    print("Publication status:     pre-activation")


if __name__ == "__main__":
    main()
