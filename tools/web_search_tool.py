from infrastructure.search_router import search_web


def web_search(
    query: str,
    max_results: int = 5,
):
    """
    Search the web for heritage and cultural information.
    """

    if not query or not query.strip():
        return []

    if max_results <= 0:
        return []

    return search_web(
        query=query,
        max_results=max_results,
    )