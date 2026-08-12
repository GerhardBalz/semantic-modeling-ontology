#!/usr/bin/env python3
"""Verify the SMO v0.1 ontology and staged pre-activation publication contract."""
from __future__ import annotations

import json
from pathlib import Path
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "model/publication-contract.json"
BACKENDS_PATH = ROOT / "publication/backend-targets.json"
W3ID_PATH = ROOT / "publication/w3id/.htaccess"
W3ID_README_PATH = ROOT / "publication/w3id/README.md"
README_PATH = ROOT / "README.md"
DOC_PATH = ROOT / "docs/namespace-publication-versioning.md"

EXPECTED_NAMESPACE = "https://w3id.org/smo#"
EXPECTED_ONTOLOGY_IRI = "https://w3id.org/smo"
EXPECTED_VERSION_IRI = "https://w3id.org/smo/0.1.0"
EXPECTED_VERSION = "0.1.0"
EXPECTED_CLASSES = {"SemanticModel", "ImplementationProjection"}
EXPECTED_DEFINITIONS = {
    "SemanticModel": "A formal representation that gives knowledge explicit machine-interpretable meaning through concepts, relationships, constraints, axioms, or equivalent semantic structures.",
    "ImplementationProjection": "A non-authoritative implementation-facing projection derived from selected semantics of a Semantic Model, preserving explicit semantic identity and relationships according to a declared preservation, transformation, introduction, and omission policy while allowing target-specific implementation concerns.",
}
FORBIDDEN_ESKA_FRAGMENTS = {"capability", "execution", "result", "verification", "service", "agent", "deployment"}
GITHUB_IDENTITY_PREFIX = "https://github.com/GerhardBalz/semantic-modeling-ontology"
RAW_BACKEND_PREFIX = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/"
CURRENT_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/main/model/smo.ttl"
VERSION_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def local_name(uri: URIRef) -> str:
    text = str(uri)
    require(text.startswith(EXPECTED_NAMESPACE), f"not an SMO term IRI: {text}")
    return text[len(EXPECTED_NAMESPACE):]


def main() -> None:
    contract = read_json(CONTRACT_PATH)
    backends = read_json(BACKENDS_PATH)
    graph = Graph()
    graph.parse(ROOT / contract["ontology"]["path"], format="turtle")

    require(contract["contractVersion"] == "1.0", "unexpected publication contract version")
    require(contract["status"] == "pre-activation", "SMO must remain pre-activation until live W3ID verification")
    require(contract["repository"] == "GerhardBalz/semantic-modeling-ontology", "repository mismatch")
    require(contract["termNamespace"]["current"] == EXPECTED_NAMESPACE, "term namespace mismatch")
    require(contract["termNamespace"]["activationStatus"] == "not-active", "namespace must not yet claim activation")
    require(contract["termNamespace"]["resolver"] == EXPECTED_ONTOLOGY_IRI, "resolver mismatch")

    ontology_iri = URIRef(EXPECTED_ONTOLOGY_IRI)
    require((ontology_iri, RDF.type, OWL.Ontology) in graph, "expected ontology IRI is not declared")
    require(graph.value(ontology_iri, OWL.versionIRI) == URIRef(EXPECTED_VERSION_IRI), "owl:versionIRI mismatch")
    require(graph.value(ontology_iri, OWL.versionInfo) == Literal(EXPECTED_VERSION), "owl:versionInfo mismatch")
    require(contract["ontology"]["ontologyIri"] == EXPECTED_ONTOLOGY_IRI, "contract ontology IRI mismatch")
    require(contract["ontology"]["versionIri"] == EXPECTED_VERSION_IRI, "contract version IRI mismatch")
    require(contract["ontology"]["version"] == EXPECTED_VERSION, "contract semantic version mismatch")

    owned_uris: set[URIRef] = set()
    for triple in graph:
        for value in triple:
            if isinstance(value, URIRef) and str(value).startswith(EXPECTED_NAMESPACE):
                owned_uris.add(value)
    owned_locals = {local_name(uri) for uri in owned_uris}
    require(owned_locals == EXPECTED_CLASSES, f"unexpected SMO-owned terms: {sorted(owned_locals)}")
    declared_classes = {local_name(s) for s in graph.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef) and str(s).startswith(EXPECTED_NAMESPACE)}
    require(declared_classes == EXPECTED_CLASSES, f"expected exactly two SMO classes, found {sorted(declared_classes)}")
    require(contract["ownedTerms"]["classes"] == ["SemanticModel", "ImplementationProjection"], "class inventory changed")
    require(contract["ownedTerms"]["objectProperties"] == [], "v0.1 must not own object properties")
    require(contract["ownedTerms"]["datatypeProperties"] == [], "v0.1 must not own datatype properties")

    for property_type in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
        owned = [s for s in graph.subjects(RDF.type, property_type) if isinstance(s, URIRef) and str(s).startswith(EXPECTED_NAMESPACE)]
        require(not owned, f"v0.1 must not mint SMO properties: {owned}")

    for name, expected_definition in EXPECTED_DEFINITIONS.items():
        term = URIRef(EXPECTED_NAMESPACE + name)
        require(list(graph.objects(term, RDFS.comment)) == [Literal(expected_definition, lang="en")], f"{name}: definition mismatch")
        labels = list(graph.objects(term, RDFS.label))
        require(len(labels) == 1 and isinstance(labels[0], Literal) and labels[0].language == "en", f"{name}: English label required")

    for name in owned_locals:
        require(not any(fragment in name.lower() for fragment in FORBIDDEN_ESKA_FRAGMENTS), f"ESKA-specific concept leaked into SMO: {name}")

    github_semantic_uris = {str(value) for triple in graph for value in triple if isinstance(value, URIRef) and str(value).startswith(GITHUB_IDENTITY_PREFIX)}
    require(not github_semantic_uris, f"GitHub URL used as semantic identity: {sorted(github_semantic_uris)}")

    require(backends["contractVersion"] == contract["contractVersion"], "backend contract version mismatch")
    require(backends["status"] == "pre-activation", "backend targets must remain pre-activation")
    require(backends["repository"] == contract["repository"], "backend repository mismatch")
    require(backends["branch"] == "main", "current publication backend must target main")
    routes = {entry["kind"]: entry for entry in backends["routes"]}
    require(set(routes) == {"current", "version"}, "expected planned current and version backend metadata")
    require(routes["current"]["route"] == EXPECTED_ONTOLOGY_IRI, "current W3ID route mismatch")
    require(routes["current"]["target"] == CURRENT_RAW, "current backend mismatch")
    require(routes["version"]["route"] == EXPECTED_VERSION_IRI, "planned version IRI mismatch")
    require(routes["version"]["target"] == VERSION_RAW, "planned immutable backend mismatch")
    require(routes["version"].get("requiresTag") == "smo-v0.1.0", "immutable target must require smo-v0.1.0")
    for entry in routes.values():
        require(entry["active"] is False, f"prepared route must not claim activation: {entry['route']}")
        require(entry["target"].startswith(RAW_BACKEND_PREFIX), f"backend outside governed repository: {entry['target']}")

    require(contract["publication"]["w3idRequested"] is False, "repository must not claim request before upstream submission")
    require(contract["publication"]["w3idActive"] is False, "repository must not claim activation")
    require(contract["releaseVersioning"]["releaseCreated"] is False, "repository must not claim release/tag")

    htaccess = W3ID_PATH.read_text(encoding="utf-8")
    require("PRE-ACTIVATION" in htaccess, "W3ID payload must be visibly pre-activation")
    require(CURRENT_RAW in htaccess, "W3ID activation payload missing current Turtle backend")
    require(VERSION_RAW not in htaccess, "immutable version redirect must not be submitted before smo-v0.1.0 exists")
    require("text/turtle" in htaccess and "R=303" in htaccess, "activation payload must support Turtle negotiation with 303 redirects")
    require("https://github.com/GerhardBalz/semantic-modeling-ontology" in htaccess, "activation payload missing human project route")

    w3id_readme = W3ID_README_PATH.read_text(encoding="utf-8")
    for token in ("@GerhardBalz", EXPECTED_ONTOLOGY_IRI, EXPECTED_NAMESPACE, "smo-v0.1.0", "no immutable version redirect"):
        require(token in w3id_readme, f"W3ID README missing governance token: {token}")

    required_tokens = (EXPECTED_NAMESPACE, EXPECTED_ONTOLOGY_IRI, EXPECTED_VERSION_IRI, EXPECTED_VERSION, "pre-activation", "smo-v0.1.0")
    for path in (README_PATH, DOC_PATH):
        text = path.read_text(encoding="utf-8")
        for token in required_tokens:
            require(token in text, f"{path.relative_to(ROOT)} missing publication-contract token: {token}")

    print("SUCCESS: SMO v0.1 ontology and staged W3ID activation payload are machine-verifiable.")
    print(f"Term namespace:       {EXPECTED_NAMESPACE}")
    print(f"Ontology IRI:         {EXPECTED_ONTOLOGY_IRI}")
    print(f"Version IRI:          {EXPECTED_VERSION_IRI}")
    print(f"Declared classes:     {len(declared_classes)}")
    print("SMO-owned properties: 0")
    print("W3ID activation:      current routes only; version route deferred")


if __name__ == "__main__":
    main()
