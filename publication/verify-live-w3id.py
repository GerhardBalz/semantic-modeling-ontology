#!/usr/bin/env python3

"""Verify the live SMO W3ID current namespace after upstream activation.

This script is intentionally prepared before activation but must only be treated
as publication evidence after perma-id/w3id.org#6538 has merged and the live
resolver has been observed externally.
"""

from __future__ import annotations

import sys
import urllib.request

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, OWL

BASE = "https://w3id.org/smo"
DIST = "https://w3id.org/smo/dist/smo.ttl"
SEMANTIC_MODEL = URIRef("https://w3id.org/smo#SemanticModel")
IMPLEMENTATION_PROJECTION = URIRef("https://w3id.org/smo#ImplementationProjection")


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


def main() -> int:
    html_url, _, _ = request(BASE, "text/html,application/xhtml+xml")
    require(
        "github.com/GerhardBalz/semantic-modeling-ontology" in html_url,
        f"HTML route resolved unexpectedly: {html_url}",
    )

    turtle_url, turtle_bytes, _ = request(BASE, "text/turtle")
    require(
        "raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/" in turtle_url,
        f"Turtle route resolved unexpectedly: {turtle_url}",
    )

    graph = Graph()
    graph.parse(data=turtle_bytes.decode("utf-8"), format="turtle")
    require((SEMANTIC_MODEL, RDF.type, OWL.Class) in graph, "SemanticModel missing from live RDF")
    require(
        (IMPLEMENTATION_PROJECTION, RDF.type, OWL.Class) in graph,
        "ImplementationProjection missing from live RDF",
    )

    dist_url, dist_bytes, _ = request(DIST, "text/turtle")
    require(
        "raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/" in dist_url,
        f"Distribution route resolved unexpectedly: {dist_url}",
    )
    require(dist_bytes == turtle_bytes, "Base Turtle and explicit distribution content differ")

    print("Verified live SMO W3ID current routes")
    print(f"HTML -> {html_url}")
    print(f"Turtle -> {turtle_url}")
    print(f"Distribution -> {dist_url}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Live W3ID verification failed: {exc}", file=sys.stderr)
        raise
