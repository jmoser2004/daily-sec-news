from typing import List, Dict
import asyncio
import aiohttp
import feedparser
from src.logger import Logger

class Feed_Handler:
    def __init__(self, feed_urls: List[str], name: str = "Feed_Handler", timeout: int = 10, logger: Logger | None = None):
        self.feed_urls = feed_urls
        self.name = name
        self.timeout = timeout
        self.logger = logger

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Dict | None:
        try:
            async with asyncio.timeout(self.timeout):
                async with session.get(url) as response:
                    if self.logger is not None:
                        self.logger.log(message=f"Navigating to {url} to get RSS feed", level="INFO")
                    html = await response.text()
                    return {"url": url, "html": html}
        except TimeoutError:
            if self.logger is not None:
                self.logger.log(message=f"{url} timed out", level="ERROR")
            return None
        except Exception as e:
            if self.logger is not None:
                self.logger.log(message=f"Error: {e}", level="ERROR")


    async def read_feeds(self) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session=session, url=url) for url in self.feed_urls]
            results = await asyncio.gather(*tasks)

        feeds = []
        for pair in results:
            if pair is None:
                continue

            html = pair["html"]
            rss = feedparser.parse(html)
            urls = [entry["link"] for entry in rss["entries"]]
            feeds.append({"base_url": pair["url"], "urls": urls})
            
            if self.logger is not None:
                self.logger.log(f"Found {len(urls)} articles at {pair["url"]}", level="INFO")

        return feeds