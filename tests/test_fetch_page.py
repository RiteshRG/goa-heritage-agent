from tools.fetch_page import fetch_page


def test_empty_url():
    result = fetch_page("")

    assert result["success"] is False
    assert result["content"] is None


def test_fetch_wikipedia_page():
    result = fetch_page(
        "https://en.wikipedia.org/wiki/Goa"
    )

    assert result["success"] is True
    assert result["title"]
    assert result["content"]

    assert "Goa" in result["content"]


def test_invalid_url():
    result = fetch_page(
        "https://this-domain-does-not-exist-12345.com"
    )

    assert result["success"] is False
    assert result["content"] is None