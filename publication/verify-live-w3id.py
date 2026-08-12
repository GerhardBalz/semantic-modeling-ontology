#!/usr/bin/env python3

"""Verify live current and immutable SMO W3ID routes.

The verifier treats W3ID redirect behavior and backend content as separate
contracts: inspect W3ID's redirect response without following browser redirects,
then fetch RDF backends independently for semantic evidence.
"""

from __future__ import annotations

import http.client
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import TypeVar

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF

BASE = "https://w3id.org/smo"
DIST = "https://w3id.org/smo/dist/smo.ttl"
VERSION = "https://w3id.org/smo/0.1.0"
VERSION_DIST = "https://w3id.org/smo/0.1.0/dist/smo.ttl"

CURRENT_HTML = "https://github.com/GerhardBalz/semantic-modeling-ontology"
CURRENT_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/main/model/smo.ttl"
VERSION_RAW = "https://raw.githubusercontent.com/GerhardBalz/semantic-modeling-ontology/smo-v0.1.0/model/smo.ttl"
VERSION_HTML = "https://github.com/GerhardBalz/semantic-modeling-ontology/blob/smo-v0.1.0/model/smo.ttl"

ONTOLOGY = URIRef(BASE)
SEMANTIC_MODEL = URIRef("https://w3id.org/smo#SemanticModel")
IMPLEMENTATION_PROJECTION = URIRef("https://w3id.org/smo#ImplementationProjection")
VERSION_IRI = URIRef(VERSION)

REDIRECT_CODES = {301, 302, 303, 307, 308}
EXPECTED_REDIRECT_CODE = 303
MAX_ATTEMPTS = 3
T = TypeVar("T")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Expose redirect responses instead of following their Location targets."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def with_retries(operation: Callable[[], T], label: str) -> T:
    """Retry transient connection failures without masking contract failures."""

    last_error: BaseException | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return operation()
        except (
            urllib.error.URLError,
            http.client.RemoteDisconnected,
            TimeoutError,
            ConnectionError,
            OSError,
        ) as exc:
            last_error = exc
            if attempt == MAX_ATTEMPTS:
                raise
            print(
                f"Transient network failure during {label} "
                f"(attempt {attempt}/{MAX_ATTEMPTS}): {exc}; retrying",
                file=sys.stderr,
            )
            time.sleep(attempt)

    raise AssertionError(f"unreachable retry state for {label}: {last_error}")


def redirect_target(url: str, accept: str) -> tuple[int, str]:
    """Return W3ID's redirect status and Location without following it."""

    def once() -> tuple[int, str]:
        request = urllib.request.Request(
            url,
            headers={"Accept": accept, "User-Agent": "SMO-live-verifier/0.2"},
        )
        opener = urllib.request.build_opener(NoRedirect)
        try:
            with opener.open(request, timeout=30) as response:
                status = getattr(response, "status", None)
                raise AssertionError(
                    f"W3ID route returned {status} without a redirect: {url}"
                )
        except urllib.error.HTTPError as exc:
            if exc.code not in REDIRECT_CODES:
                raise AssertionError(
                    f"W3ID route returned unexpected HTTP {exc.code}: {url}"
                ) from exc
            location = exc.headers.get("Location")
            require(bool(location), f"W3ID redirect omitted Location: {url}")
            return exc.code, str(location)

    return with_retries(once, f"redirect inspection for {url}")


def fetch_target(url: str, accept: str = "text/turtle") -> tuple[bytes, str]:
    """Fetch backend content separately from the W3ID redirect assertion."""

    def once() -> tuple[bytes, str]:
        request = urllib.request.Request(
            url,
            headers={"Accept": accept, "User-Agent": "SMO-live-verifier/0.2"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read(), response.headers.get("Content-Type", "")
        except urllib.error.HTTPError as exc:
            raise AssertionError(
                f"Backend target returned unexpected HTTP {exc.code}: {url}"
            ) from exc

    return with_retries(once, f"backend fetch for {url}")


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


def require_redirect(url: str, accept: str, expected_target: str, label: str) -> str:
    status, target = redirect_target(url, accept)
    require(
        status == EXPECTED_REDIRECT_CODE,
        f"{label} returned HTTP {status}, expected {EXPECTED_REDIRECT_CODE}",
    )
    require(target == expected_target, f"{label} resolved unexpectedly: {target}")
    return target


def main() -> int:
    # Current routes remain governed by main. HTML evidence is the W3ID Location;
    # do not follow it into GitHub because GitHub availability is a separate concern.
    current_html_target = require_redirect(
        BASE,
        "text/html,application/xhtml+xml",
        CURRENT_HTML,
        "Current HTML route",
    )

    current_turtle_target = require_redirect(
        BASE,
        "text/turtle",
        CURRENT_RAW,
        "Current Turtle route",
    )
    turtle_bytes, _ = fetch_target(current_turtle_target)
    current_graph = parse_graph(turtle_bytes, "current live RDF")
    require_v01_terms(current_graph, "current live RDF")

    current_dist_target = require_redirect(
        DIST,
        "text/turtle",
        CURRENT_RAW,
        "Current distribution route",
    )
    dist_bytes, _ = fetch_target(current_dist_target)
    require(dist_bytes == turtle_bytes, "Current base Turtle and distribution content differ")

    # Immutable routes must resolve only to the governed smo-v0.1.0 tag.
    version_html_target = require_redirect(
        VERSION,
        "text/html,application/xhtml+xml",
        VERSION_HTML,
        "Immutable HTML route",
    )

    version_turtle_target = require_redirect(
        VERSION,
        "text/turtle",
        VERSION_RAW,
        "Immutable Turtle route",
    )
    version_turtle_bytes, _ = fetch_target(version_turtle_target)
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

    version_dist_target = require_redirect(
        VERSION_DIST,
        "text/turtle",
        VERSION_RAW,
        "Immutable distribution route",
    )
    version_dist_bytes, _ = fetch_target(version_dist_target)
    require(
        version_dist_bytes == version_turtle_bytes,
        "Immutable base Turtle and immutable distribution content differ",
    )

    print("Verified live SMO W3ID current and immutable v0.1.0 routes")
    print(f"Current HTML         -> {current_html_target}")
    print(f"Current Turtle       -> {current_turtle_target}")
    print(f"Current distribution -> {current_dist_target}")
    print(f"v0.1.0 HTML          -> {version_html_target}")
    print(f"v0.1.0 Turtle        -> {version_turtle_target}")
    print(f"v0.1.0 distribution  -> {version_dist_target}")
    return 0


def graph_value_equals(graph: Graph, subject: URIRef, predicate: URIRef, expected: Literal) -> bool:
    return graph.value(subject, predicate) == expected


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Live W3ID verification failed: {exc}", file=sys.stderr)
        raise
