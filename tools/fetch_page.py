import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "GoaHeritageCultureGuide/1.0 (MSc AI academic project)"
}


def fetch_page(url: str) -> dict:
    """Fetch a webpage and return readable text content."""

    if not url or not url.strip():
        return {
            "success": False,
            "url": url,
            "title": None,
            "content": None,
            "error": "URL cannot be empty.",
        }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for element in soup(
            ["script", "style", "noscript", "header", "footer", "nav"]
        ):
            element.decompose()

        title = soup.title.get_text(strip=True) if soup.title else None

        content = soup.get_text(
            separator=" ",
            strip=True,
        )

        return {
            "success": True,
            "url": url,
            "title": title,
            "content": content,
            "error": None,
        }

    except requests.RequestException as exc:
        return {
            "success": False,
            "url": url,
            "title": None,
            "content": None,
            "error": f"Page request failed: {exc}",
        }