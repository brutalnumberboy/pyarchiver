import requests
from bs4 import BeautifulSoup
import os

class Cralwer:
    def __init__(self):
        urls_to_visit = ['https://www.google.com']
        self.urls_to_visit = urls_to_visit


    def crawl_links(self):
        """
        Crawl a given website and discover links.
        """
        counter = 0
        discovered_urls = set()
        while self.urls_to_visit and counter < 1:
            url = self.urls_to_visit.pop(0)
            response = requests.get(url=url)
            response.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select("a[href]")
            for link in links:
                url = link.get('href')
                if url.startswith('http' or 'https'):
                    if url not in discovered_urls:
                        discovered_urls.add(url)
                    self.urls_to_visit.append(url)
            counter += 1
        return discovered_urls
    
    def extract_html(self, url):
        """
        Extract HTML and write to a file
        """
        response = requests.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        if response.status_code == 200:
            os.makedirs("html", exist_ok=True)
            with open("html/" + title + '.html', 'w') as file:
                file.write(soup.prettify())

    
    def write_to_file(self, urls):
        """
        Write discovered URLs to a file
        """
        for url in urls:
            with open('urls.txt', 'a+') as file:
                file.seek(0)
                if (url + '\n') not in file.read():
                    file.write(url + '\n')

        print(f"Discovered {len(urls)} URLs. Check urls.txt for the list.")

    