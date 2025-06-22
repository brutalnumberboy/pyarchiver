import cssutils
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

def extract_css(url):
    """
    Extracts external and inline CSS.
    """
    css_files = []
    inline_styles = []
    response = requests.get(url=url)
    response.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(response.text, 'html.parser')
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

