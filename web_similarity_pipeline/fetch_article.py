import requests
from readability import Document
from bs4 import BeautifulSoup

def fetch_full_article(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        html = response.text

        doc = Document(html)
        soup = BeautifulSoup(doc.summary(), "html.parser")
        text = soup.get_text(separator=" ")

        return text.strip()
    except Exception as e:
        return None

