import crawl_links
import get_images

def main():
    crawler = crawl_links.Cralwer()
    urls = crawler.crawl_links()
    crawler.write_to_file(urls)
    get_images.get_images()


if __name__ == "__main__":
    main()