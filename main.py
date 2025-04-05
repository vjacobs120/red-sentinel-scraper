from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from bs4 import BeautifulSoup
import requests

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: HttpUrl

@app.post("/scrape")
def scrape_url(payload: ScrapeRequest):
    try:
        response = requests.get(payload.url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("article") or soup.find("main") or soup.body
        content = article.get_text(separator="\n", strip=True) if article else "No readable content found."
        return {"url": payload.url, "content": content}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Scraping failed: {str(e)}"}
@app.get("/health")
def health_check():
    return {"status": "ok"}
