import pytest

from infrastructure.search_router import search_web
from tools.web_search_tool import web_search


def test_empty_query():
    result = web_search("")

    assert result == []


def test_invalid_max_results():
    result = web_search(
        "Goa heritage",
        max_results=0,
    )

    assert result == []


def test_web_search_returns_results():
    results = web_search(
        "Goa heritage",
        max_results=3,
    )

    assert isinstance(results, list)

    for result in results:
        assert result.title
        assert result.url
        assert result.snippet