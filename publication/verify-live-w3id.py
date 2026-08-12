#!/usr/bin/env python3

"""Verify live current and immutable SMO W3ID routes.

The immutable checks become publication evidence only after the upstream W3ID
version-route pull request has merged and these routes have been observed live.
"""

from __future__ import annotations

import sys
import urllib.request

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, OWL

BASE = "https://w3id.org/smo"
DIST = "https://w3id.org/smo/dist/smo.ttl"
VERSION = "https://w3id.org/smo/0.1.0"
VERSION_DIST = "https://w3id.org/smo/0.1.0/dist/smo.ttl"

CURRENT_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/main/model/smo.ttl"
VERSION_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl"
VERSION_HTML = "https://github.com/GerhardBalz/semantic-modeling-ontology/blob/smo-v0.1.0/model/smo.ttl"

ONTOLOGY = URIRef(BASE)
SEMANTIC_MODEL = URIRef("https://w3id.org/smo#SemanticModel")
IMPLEMENTATION_PROJECTION = URIRef("https://w3id.org/smo#ImplementationProjection")
VERSION_IRI = URIRef(VERSION)


def request(url: str, accept: str) -> tuple[str, bytes, str]:
    req = urllib.request.Request(
        url,
        headers={"Accept": accept, "User-Agent": "SMO-live-verifier/0.1"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.geturl(), response.read(), response.headers.get("Content-Type", "")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_graph(data: bytes, label: str) -> Graph:
    graph = Graph()
    try:
        graph.parse(data=data.decode("utf-8"), format="turtle")
    except Exception as exc:
        raise AssertionError(f"{label} is not valid Turtle: {exc}") from exc
    return graph


def require_v01_terms(graph: Graph, label: str) -> None:
    require(
        (SEMANTIC_MODEL, RDF.type, OWL.Class) in graph,
        f"SemanticModel missing from {label}",
    )
    require(
        (IMPLEMENTATION_PROJECTION, RDF.type, OWL.Class) in graph,
        f"ImplementationProjection missing from {label}",
    )


def main() -> int:
    # Current routes remain governed by main.
    html_url, _, _ = request(BASE, "text/html,application/xhtml+xml")
    require(
        "github.com/GerhardBalz/semantic-modeling-ontology" in html_url,
        f"Current HTML route resolved unexpectedly: {html_url}",
    )

    turtle_url, turtle_bytes, _ = request(BASE, "text/turtle")
    require(
        CURRENT_RAW in turtle_url,
        f"Current Turtle route resolved unexpectedly: {turtle_url}",
    )
    current_graph = parse_graph(turtle_bytes, "current live RDF")
    require_v01_terms(current_graph, "current live RDF")

    dist_url, dist_bytes, _ = request(DIST, "text/turtle")
    require(
        CURRENT_RAW in dist_url,
        f"Current distribution route resolved unexpectedly: {dist_url}",
    )
    require(dist_bytes == turtle_bytes, "Current base Turtle and distribution content differ")

    # Immutable routes must resolve only to the governed smo-v0.1.0 tag.
    version_html_url, _, _ = request(VERSION, "text/html,application/xhtml+xml")
    require(
        VERSION_HTML in version_html_url,
        f"Immutable HTML route resolved unexpectedly: {version_html_url}",
    )

    version_turtle_url, version_turtle_bytes, _ = request(VERSION, "text/turtle")
    require(
        VERSION_RAW in version_turtle_url,
        f"Immutable Turtle route resolved unexpectedly: {version_turtle_url}",
    )
    version_graph = parse_graph(version_turtle_bytes, "immutable v0.1.0 RDF")
    require_v01_terms(version_graph, "immutable v0.1.0 RDF")
    require(
        (ONTOLOGY, OWL.versionIRI, VERSION_IRI) in version_graph,
        "Immutable v0.1.0 RDF does not declare the expected owl:versionIRI",
    )
    require(
        graph_value_equals(version_graph, ONTOLOGY, OWL.versionInfo, Literal("0.1.0")),
        "Immutable v0.1.0 RDF does not declare owl:versionInfo 0.1.0",
    )

    version_dist_url, version_dist_bytes, _ = request(VERSION_DIST, "text/turtle")
    require(
        VERSION_RAW in version_dist_url,
        f"Immutable distribution route resolved unexpectedly: {version_dist_url}",
    )
    require(
        version_dist_bytes == version_turtle_bytes,
        "Immutable base Turtle and immutable distribution content differ",
    )

    print("Verified live SMO W3ID current and immutable v0.1.0 routes")
    print(f"Current HTML         -> {html_url}")
    print(f"Current Turtle       -> {turtle_url}")
    print(f"Current distribution -> {dist_url}")
    print(f"v0.1.0 HTML          -> {version_html_url}")
    print(f"v0.1.0 Turtle        -> {version_turtle_url}")
    print(f"v0.1.0 distribution  -> {version_dist_url}")
    return 0


def graph_value_equals(graph: Graph, subject: URIRef, predicate: URIRef, expected: Literal) -> bool:
    return graph.value(subject, predicate) == expected


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Live W3ID verification failed: {exc}", file=sys.stderr)
        raise
