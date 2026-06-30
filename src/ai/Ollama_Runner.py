from typing import Dict, List
import requests
from src.logger import Logger

class Ollama_Runner:
    def __init__(self, url: str, prompts: Dict, model: Dict, name: str = "Ollama_Runner", logger: Logger | None = None):
        self.url = url
        self.prompts = prompts
        self.model = model
        self.name = name
        self.logger = logger

    def chat(self, prompts: List[Dict]) -> str:
        model_name = self.model["full_tag"]
        
        payload = {
            "model": model_name,
            "messages": prompts,
            "stream": False
        }

        response = requests.post(self.url, json=payload)
        return response.json()["message"]["content"]
    
    def summarize_article(self, article: str):
        system = self.prompts["summarize"]["system"]

        prompts = [{"role": "system", "content": system}, {"role": "user", "content": article}]

        return self.chat(prompts=prompts)
    
    def rank_articles(self, articles: List[str]):
        system = self.prompts["rank"]["system"]

        prompts = [{"role": "system", "content": system}]

        for article in articles:
            prompts.append(article)

        return self.chat(prompts=prompts)