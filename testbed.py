import asyncio
from src.feed.feed_handler import Feed_Handler
from src.feed.article_scraper import Article_Scraper
from config import Config
from src.logger import Logger
from src.ai import Ollama_Runner

async def test():
    """
    path = "logs/feed.log"
    nl = 15
    fh = Feed_Handler(feed_urls=["https://thehackernews.com/feeds/posts/default"],logger=Logger(name="feedhandler", path=path, name_length=nl))
    results = await fh.read_feeds()
    for result in results:
        urls = result["urls"]
        artscr = Article_Scraper(urls=urls, tags={"article_tag": "div#articlebody", "paragraph_tag": "p"}, base_url=result["base_url"], logger=Logger(name=f"{result["base_url"] + "-scraper"}", path=path, name_length=nl))
        scraped = await artscr.scrape_articles()
    """

    feed_config = Config(path="config/yml/feed/feed.yml", logger=Logger(name="feed_config", path="logs/feed.log"))
    ai_config = Config(path="config/yml/ai/ollama.yml", logger=Logger(name="ollama_config", path="logs/ai.log"))

    fhfc = feed_config.get_config("feed_handler")
    feed_handler = Feed_Handler(feed_urls=fhfc["feed_urls"], logger=Logger(name=fhfc["logger"]["name"], path=fhfc["logger"]["path"], log_to_console=fhfc["logger"]["log_to_console"]))

    results = await feed_handler.read_feeds()
    print(results[0])

    asfc = feed_config.get_config("article_scraper")

    scraper = Article_Scraper(urls=results[0]["urls"], tags=asfc["scrapers"][0]["tags"], base_url=asfc["scrapers"][0]["base_url"])

    scraped = await scraper.scrape_articles()
    
    ai_url_conf = ai_config.get_config("url")
    ai_url = ai_url_conf["protocol"] + "://" + ai_url_conf["base_url"] + ":" + ai_url_conf["port"]
    for dir in ai_url_conf["dirs"]:
        ai_url += "/" + dir
    
    prompt_conf = ai_config.get_config("prompts")
    model_conf = ai_config.get_config("models")[0]

    ai = Ollama_Runner(url=ai_url, prompts=prompt_conf, model=model_conf)

    for article in scraped:
        print(ai.summarize_article(article=article))


asyncio.run(test())
