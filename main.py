import crawl_links
import write_to_file
import get_images

def main():
    urls = crawl_links.crawl_links()
    write_to_file.write_to_file(urls)
    get_images.get_images()


if __name__ == "__main__":
    main()