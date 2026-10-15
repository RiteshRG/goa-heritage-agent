import requests

HEADERS = {
    "User-Agent": "GoaHeritageCultureGuide/1.0 (MSc AI academic project)"
}

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def lookup_wikipedia(query: str) -> dict:
    """
    Search Wikipedia and return the best matching page.
    """

    if not query or not query.strip():
        return {
            "success": False,
            "query": query,
            "title": None,
            "url": None,
            "summary": None,
            "error": "Query cannot be empty.",
        }

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=HEADERS,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        search_results = data.get("query", {}).get("search", [])

        if not search_results:
            return {
                "success": False,
                "query": query,
                "title": None,
                "url": None,
                "summary": None,
                "error": "No Wikipedia page found.",
            }

        page = search_results[0]

        title = page["title"]

        page_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "exintro": True,
            "explaintext": True,
            "inprop": "url",
            "titles": title,
        }

        page_response = requests.get(
            WIKIPEDIA_API_URL,
            params=page_params,
            headers=HEADERS,
            timeout=10,
        )

        page_response.raise_for_status()

        page_data = page_response.json()

        pages = page_data.get("query", {}).get("pages", {})

        page_info = next(iter(pages.values()))

        return {
            "success": True,
            "query": query,
            "title": page_info.get("title"),
            "url": page_info.get("fullurl"),
            "summary": page_info.get("extract"),
            "error": None,
        }

    except requests.RequestException as exc:
        return {
            "success": False,
            "query": query,
            "title": None,
            "url": None,
            "summary": None,
            "error": f"Wikipedia request failed: {exc}",
        }

    except (ValueError, KeyError, StopIteration) as exc:
        return {
            "success": False,
            "query": query,
            "title": None,
            "url": None,
            "summary": None,
            "error": f"Invalid Wikipedia response: {exc}",
        }