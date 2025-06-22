def write_to_file(urls):
    """
    Write discovered URLs to a file
    """
    for url in urls:
        with open('urls.txt', 'a+') as file:
            file.seek(0)
            if (url + '\n') not in file.read():
                file.write(url + '\n')

    print(f"Discovered {len(urls)} URLs. Check urls.txt for the list.")