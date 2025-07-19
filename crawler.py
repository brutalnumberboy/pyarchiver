import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import cssutils


class Cralwer:
    def __init__(self, urls, depth=1):
        self.urls_to_visit = urls
        self.depth = depth


    def crawl_links(self):
        """
        Crawl a given website and discover links.
        """
        counter = 0
        discovered_urls = set()
        while self.urls_to_visit and counter < self.depth:
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
    
    def extract_html(self, urls):
        """
        Extract HTML and write to a file
        """
        url = urls.pop()
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

    def extract_css(self, urls):
        """
        Extracts external and inline CSS.
        """
        css_files = []
        inline_styles = []
        url = urls.pop()
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if response.status_code == 200:
            os.makedirs("styles", exist_ok=True)
            for css in soup.find_all("link"):
                # find external css files
                if css.attrs.get("href"):
                    # if the link tag has the 'href' attribute
                    css_url = urljoin(url, css.attrs.get("href"))
                    if "css" in css_url:
                        response = requests.get(css_url, stream=True)
                        print(cssutils.parseString(response.text))
                        with open("styles/" + css_url.split("/")[-1], "wb") as file:
                            file.write(response.content)
        
        for style in soup.find_all("style"):
            # find inline css 
            if style.string:
                inline_styles.append(cssutils.parseStyle(style.string))
        print(css_files)


    def get_images(self, urls):
        counter = 0
        while urls and counter < self.depth:
            url = urls.pop()
            response = requests.get(url=url, stream=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            if response.status_code == 200: 
                os.makedirs("media", exist_ok=True)
                for img in images:
                    img_url = img.get('src')
                    if img_url and (img_url.startswith('http') or img_url.startswith('https')):
                        response = requests.get(img_url, stream=True)
                        with open("media/" + img_url.split("/")[-1], "wb") as file:
                            file.write(response.content)
                    print(f"Image URL: {img_url}")
    