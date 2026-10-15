import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv(override=True)


SERPER_API_URL = "https://google.serper.dev/search"

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


def get_serper_api_key() -> str:
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "SERPER_API_KEY is not configured."
        )

    return api_key


def search_web(
    query: str,
    max_results: int = 5,
) -> list[SearchResult]:

    if not query or not query.strip():
        return []

    if max_results <= 0:
        return []

    api_key = get_serper_api_key()

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "q": query,
        "num": max_results,
    }

    response = requests.post(
        SERPER_API_URL,
        headers=headers,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("organic", []):
        results.append(
            SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
            )
        )

    return results