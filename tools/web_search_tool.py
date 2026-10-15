from infrastructure.search_router import search_web
from langchain.tools import tool
import json

@tool
def web_search_tool(
    query: str,
    max_results: int = 5,
):
    """
    Search the web for additional information about Goa
    heritage and culture.

    Use this when the available heritage dataset or
    Wikipedia information is insufficient.
    """

    results = web_search(
        query=query,
        max_results=max_results,
    )

    return json.dumps(
        [
            {
                "title": result.title,
                "url": result.url,
                "snippet": result.snippet,
            }
            for result in results
        ],
        ensure_ascii=False,
    )

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