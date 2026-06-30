from bs4 import BeautifulSoup
from typing import List, Dict
import asyncio
import aiohttp
from src.logger import Logger

class Article_Scraper:

    HEADERS = {"User-Agent": "Mozilla/5.0"}

    def __init__(self, urls: List[str], tags: Dict, base_url:str, name: str = "Article_Scraper", timeout: int = 10, max_concurrent: int = 10, logger: Logger | None = None):
        self.urls = urls
        self.tags = tags
        self.base_url = base_url
        self.name = name
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.logger = logger

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str | None:
        try:
            async with asyncio.timeout(self.timeout):
                async with session.get(url, headers=self.HEADERS) as response:
                    return await response.text()
        except TimeoutError:
            if self.logger is not None:
                self.logger.log(message=f"{url} timed out", level="ERROR")
            return None
        except Exception as e:
            if self.logger is not None:
                self.logger.log(message=f"Error: {e}", level="ERROR")
            return None

    async def parse_html(self, html: str) -> str | None:
        try:    
            soup = BeautifulSoup(html, "html.parser")
            
            article = soup.select_one(self.tags["article_tag"])
            if article:
                paragraphs = article.find_all(self.tags["paragraph_tag"])
                text = '\n'.join(p.get_text(strip=True) for p in paragraphs)
                return text
            else:
                self.logger.log(message=f"Could not find article with tag {self.tags['article_tag']}", level="WARN")
                return None
        except Exception as e:
            if self.logger is not None:
                self.logger.log(message=f"Error: {e}", level="ERROR")
            return None

    async def scrape_articles(self) -> List[str]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        if(self.logger is not None):
            self.logger.log(message=f"Scraping articles at {self.base_url}", level="INFO")

        async def fetch_chunk(session: aiohttp.ClientSession, url: str) -> str:
            async with semaphore:
                return await self.fetch(session=session, url=url)

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_chunk(session=session, url=url) for url in self.urls]
            raw_data = await asyncio.gather(*tasks)
        
        tasks = [self.parse_html(html=html) for html in raw_data if html is not None]
        parsed = await asyncio.gather(*tasks)

        return [text for text in parsed if text is not None]
    
    async def get_raw_html(self) -> List[str]: #For use in training models
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def fetch_chunk(session: aiohttp.ClientSession, url: str) -> str:
            async with semaphore:
                return await self.fetch(session=session, url=url)
            
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_chunk(session=session, url=url) for url in self.urls]
            raw_data = await asyncio.gather(*tasks)

        return [html for html in raw_data if html is not None]