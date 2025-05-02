from firecrawl import FirecrawlApp
from langchain.tools import tool
from app.core.config import settings

@tool
def crawl_website(url: str):
    """
    Crawl the given URL with FirecrawlApp and return the fetched pages.

    - Initializes a FirecrawlApp client using the FIRECRAWL_API_KEY from your environment.
    - Starts crawling from `url`.
    - Skips any paths matching the regex `blog/.+`.
    - Stops after fetching up to 5 pages to avoid excessive crawling.
    
    Args:
        url (str): The root URL to begin crawling.

    Returns:
        dict: The raw crawl result (e.g. a mapping of fetched URLs to their page data)
    """
    app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)
    result = app.crawl_url(
        url,
        {
            "exclude_paths": ["blog/.+"],
            "limit": 5
        }
    )
    return result
