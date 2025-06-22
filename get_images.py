import requests
from bs4 import BeautifulSoup

def get_images():
    urls_to_visit = ['https://wallhaven.cc/w/gwjq3d']
    counter = 0
    while urls_to_visit and counter < 2:
        url = urls_to_visit.pop(0)
        response = requests.get(url=url, stream=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url and (img_url.startswith('http') or img_url.startswith('https')):
                response = requests.get(img_url, stream=True)
                with open("media/" + img_url.split("/")[-1], "wb") as file:
                    file.write(response.content)
            print(f"Image URL: {img_url}")