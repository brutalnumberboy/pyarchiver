import requests
from bs4 import BeautifulSoup

def crawl_links():
    """
    Crawl a given website and discover links.
    """
    urls_to_visit = ['https://www.google.com']
    counter = 0
    discovered_urls = set()
    while urls_to_visit and counter < 2:
        url = urls_to_visit.pop(0)
        response = requests.get(url=url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select("a[href]")
        for link in links:
            url = link.get('href')
            if url.startswith('http' or 'https'):
                if url not in discovered_urls:
                    discovered_urls.add(url)
                urls_to_visit.append(url)
        counter += 1
    return discovered_urls

    