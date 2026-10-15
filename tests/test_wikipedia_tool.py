from tools.wikipedia_tool import lookup_wikipedia
import pytest

def test_empty_query():
    result = lookup_wikipedia("")

    assert result["success"] is False
    assert result["error"] is not None

def test_wikipedia_search():
    result = lookup_wikipedia("Basilica of Bom Jesus Goa")

    assert result["success"] is True
    assert result["title"]
    assert result["url"]
    assert result["summary"]


def test_wikipedia_unknown_place():
    result = lookup_wikipedia(
        "xyzabc123_this_place_should_not_exist_987654"
    )

    assert result["success"] is False