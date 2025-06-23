import crawl_links
import get_images
import extract_css

def main():
    crawler = crawl_links.Cralwer()
    urls = crawler.crawl_links()
    # crawler.write_to_file(urls)
    # get_images.get_images()
    crawler.extract_html('https://wallhaven.cc/w/gwjq3d')
    extract_css.extract_css('https://wallhaven.cc/w/gwjq3d')


if __name__ == "__main__":
    main()