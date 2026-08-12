#!/usr/bin/env python3
"""Verify the SMO v0.1 ontology and current-active publication contract."""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model/publication-contract.json"
BACKENDS = ROOT / "publication/backend-targets.json"
README = ROOT / "README.md"
DOC = ROOT / "docs/namespace-publication-versioning.md"

NS = "https://w3id.org/smo#"
ONTOLOGY = "https://w3id.org/smo"
VERSION_IRI = "https://w3id.org/smo/0.1.0"
VERSION = "0.1.0"
W3ID_PR = "https://github.com/perma-id/w3id.org/pull/6538"
W3ID_MERGE = "42367a77c52b60dab4cdf55327fca023e78a61a4"
LIVE_RUN = "https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31627245287"
CURRENT_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/main/model/smo.ttl"
VERSION_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl"
EXPECTED_CLASSES = {"SemanticModel", "ImplementationProjection"}
EXPECTED_DEFINITIONS = {
    "SemanticModel": "A formal representation that gives knowledge explicit machine-interpretable meaning through concepts, relationships, constraints, axioms, or equivalent semantic structures.",
    "ImplementationProjection": "A non-authoritative implementation-facing projection derived from selected semantics of a Semantic Model, preserving explicit semantic identity and relationships according to a declared preservation, transformation, introduction, and omission policy while allowing target-specific implementation concerns.",
}
FORBIDDEN = {"capability", "execution", "result", "verification", "service", "agent", "deployment"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def local(uri: URIRef) -> str:
    text = str(uri)
    require(text.startswith(NS), f"not an SMO term IRI: {text}")
    return text[len(NS):]


def main() -> None:
    contract = load(CONTRACT)
    backends = load(BACKENDS)
    graph = Graph()
    graph.parse(ROOT / contract["ontology"]["path"], format="turtle")

    require(contract["contractVersion"] == "1.0", "unexpected contract version")
    require(contract["status"] == "current-active", "current publication must be active")
    require(contract["repository"] == "GerhardBalz/semantic-modeling-ontology", "repository mismatch")
    require(contract["termNamespace"] == {
        "current": NS,
        "activationStatus": "active",
        "resolver": ONTOLOGY,
    }, "term namespace publication state mismatch")

    ontology = URIRef(ONTOLOGY)
    require((ontology, RDF.type, OWL.Ontology) in graph, "ontology IRI not declared")
    require(graph.value(ontology, OWL.versionIRI) == URIRef(VERSION_IRI), "version IRI mismatch")
    require(graph.value(ontology, OWL.versionInfo) == Literal(VERSION), "version mismatch")
    require(contract["ontology"] == {
        "path": "model/smo.ttl",
        "ontologyIri": ONTOLOGY,
        "versionIri": VERSION_IRI,
        "version": VERSION,
    }, "ontology contract mismatch")

    declared = {
        local(subject)
        for subject in graph.subjects(RDF.type, OWL.Class)
        if isinstance(subject, URIRef) and str(subject).startswith(NS)
    }
    require(declared == EXPECTED_CLASSES, f"unexpected SMO classes: {sorted(declared)}")
    require(contract["ownedTerms"]["classes"] == ["SemanticModel", "ImplementationProjection"], "class inventory changed")
    require(contract["ownedTerms"]["objectProperties"] == [], "SMO v0.1 must not own object properties")
    require(contract["ownedTerms"]["datatypeProperties"] == [], "SMO v0.1 must not own datatype properties")

    for property_type in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
        owned = [s for s in graph.subjects(RDF.type, property_type) if isinstance(s, URIRef) and str(s).startswith(NS)]
        require(not owned, f"SMO v0.1 must not mint properties: {owned}")

    for name, definition in EXPECTED_DEFINITIONS.items():
        term = URIRef(NS + name)
        require(list(graph.objects(term, RDFS.comment)) == [Literal(definition, lang="en")], f"{name} definition mismatch")
        labels = list(graph.objects(term, RDFS.label))
        require(len(labels) == 1 and labels[0].language == "en", f"{name} English label required")
        require(not any(fragment in name.lower() for fragment in FORBIDDEN), f"ESKA-specific concept leaked into SMO: {name}")

    publication = contract["publication"]
    require(publication["w3idRequested"] is True, "W3ID request must be recorded")
    require(publication["w3idPullRequest"] == W3ID_PR, "W3ID PR mismatch")
    require(publication["w3idMergeCommit"] == W3ID_MERGE, "W3ID merge commit mismatch")
    require(publication["w3idActive"] is True, "current W3ID route must be active")
    require(publication["liveVerificationRun"] == LIVE_RUN, "live verification evidence mismatch")
    require(contract["releaseVersioning"]["releaseCreated"] is False, "release must remain unpublished at current-active stage")

    require(backends["status"] == "current-active", "backend status mismatch")
    routes = {entry["kind"]: entry for entry in backends["routes"]}
    require(set(routes) == {"current", "version"}, "expected current and version routes")
    current = routes["current"]
    version = routes["version"]
    require(current["route"] == ONTOLOGY and current["target"] == CURRENT_RAW and current["active"] is True, "current backend mismatch")
    require(current["activationRequest"] == W3ID_PR, "current activation request mismatch")
    require(current["activationMergeCommit"] == W3ID_MERGE, "current merge evidence mismatch")
    require(current["liveVerificationRun"] == LIVE_RUN, "current live evidence mismatch")
    require(version["route"] == VERSION_IRI and version["target"] == VERSION_RAW, "version backend mismatch")
    require(version["active"] is False, "immutable route must remain inactive before release")
    require(version["requiresTag"] == "smo-v0.1.0", "immutable route must require governed tag")

    for path in (README, DOC):
        text = path.read_text(encoding="utf-8")
        for token in (NS, ONTOLOGY, VERSION_IRI, "current-active", "6538", "smo-v0.1.0"):
            require(token in text, f"{path.relative_to(ROOT)} missing token: {token}")

    print("SUCCESS: SMO v0.1 ontology and current-active publication state are machine-verifiable.")
    print(f"Term namespace:       {NS}")
    print(f"Ontology IRI:         {ONTOLOGY}")
    print(f"Version IRI:          {VERSION_IRI}")
    print("Declared classes:     2")
    print("SMO-owned properties: 0")
    print("W3ID current route:   active and live-verified")
    print("Immutable route:      deferred until smo-v0.1.0 exists")


if __name__ == "__main__":
    main()
