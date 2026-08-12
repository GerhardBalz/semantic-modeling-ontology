#!/usr/bin/env python3
"""Verify the SMO v0.1 ontology and release-published publication contract."""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model/publication-contract.json"
BACKENDS = ROOT / "publication/backend-targets.json"
RELEASE_MANIFEST = ROOT / "publication/releases/smo-v0.1.0.json"
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
RELEASE_TAG = "smo-v0.1.0"
RELEASE_COMMIT = "e6ab3f8cf14bafae466a0150ad356547f164bdab"
RELEASE_URL = "https://github.com/GerhardBalz/semantic-modeling-ontology/releases/tag/smo-v0.1.0"
RELEASE_RUN = "https://github.com/GerhardBalz/semantic-modeling-ontology/actions/runs/31633781524"
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
    manifest = load(RELEASE_MANIFEST)
    graph = Graph()
    graph.parse(ROOT / contract["ontology"]["path"], format="turtle")

    require(contract["contractVersion"] == "1.0", "unexpected contract version")
    require(contract["status"] == "release-published", "governed release publication must be recorded")
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

    release = contract["releaseVersioning"]
    require(release["repositoryTagPattern"] == "smo-v{version}", "repository tag pattern mismatch")
    require(release["initialRepositoryVersion"] == VERSION, "initial repository version mismatch")
    require(release["releaseCreated"] is True, "governed release must be recorded")
    require(release["releaseTag"] == RELEASE_TAG, "release tag mismatch")
    require(release["releaseCommit"] == RELEASE_COMMIT, "release commit mismatch")
    require(release["releaseUrl"] == RELEASE_URL, "release URL mismatch")
    require(release["releaseWorkflowRun"] == RELEASE_RUN, "release workflow evidence mismatch")
    require(release["immutableBackend"] == VERSION_RAW, "immutable release backend mismatch")
    require(release["immutableBackendVerified"] is True, "immutable release backend must be verified")
    require(release["termIrisUnversioned"] is True, "SMO term IRIs must remain unversioned")

    require(manifest["release"] == RELEASE_TAG, "release manifest tag mismatch")
    require(manifest["repositoryVersion"] == VERSION, "release manifest version mismatch")
    require(manifest["termNamespace"] == NS, "release manifest namespace mismatch")
    require(manifest["ontologyIri"] == ONTOLOGY, "release manifest ontology IRI mismatch")
    require(manifest["ontologyVersionIri"] == VERSION_IRI, "release manifest version IRI mismatch")
    require(manifest["ownedTerms"] == contract["ownedTerms"], "release manifest term inventory mismatch")

    require(backends["status"] == "release-published", "backend status mismatch")
    routes = {entry["kind"]: entry for entry in backends["routes"]}
    require(set(routes) == {"current", "version"}, "expected current and version routes")
    current = routes["current"]
    version = routes["version"]
    require(current["route"] == ONTOLOGY and current["target"] == CURRENT_RAW and current["active"] is True, "current backend mismatch")
    require(current["activationRequest"] == W3ID_PR, "current activation request mismatch")
    require(current["activationMergeCommit"] == W3ID_MERGE, "current merge evidence mismatch")
    require(current["liveVerificationRun"] == LIVE_RUN, "current live evidence mismatch")
    require(version["route"] == VERSION_IRI and version["target"] == VERSION_RAW, "version backend mismatch")
    require(version["active"] is False, "immutable W3ID route must remain inactive before upstream activation")
    require(version["requiresTag"] == RELEASE_TAG, "immutable route must require governed tag")
    require(version["releaseExists"] is True, "version backend must record existing release")
    require(version["releaseCommit"] == RELEASE_COMMIT, "version backend release commit mismatch")
    require(version["backendVerified"] is True, "version backend must be recorded verified")

    for path in (README, DOC):
        text = path.read_text(encoding="utf-8")
        for token in (NS, ONTOLOGY, VERSION_IRI, "release-published", "6538", RELEASE_TAG, RELEASE_COMMIT):
            require(token in text, f"{path.relative_to(ROOT)} missing token: {token}")

    print("SUCCESS: SMO v0.1 ontology and release-published publication state are machine-verifiable.")
    print(f"Term namespace:       {NS}")
    print(f"Ontology IRI:         {ONTOLOGY}")
    print(f"Version IRI:          {VERSION_IRI}")
    print("Declared classes:     2")
    print("SMO-owned properties: 0")
    print("W3ID current route:   active and live-verified")
    print(f"Governed release:     {RELEASE_TAG} at {RELEASE_COMMIT}")
    print("Immutable backend:    verified")
    print("Immutable W3ID route: pending upstream activation")


if __name__ == "__main__":
    main()
