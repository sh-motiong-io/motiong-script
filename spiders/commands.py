import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import uuid
import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# instance of Options class allows
# us to configure Headless Chrome
options = Options()

# it should be run without UI (Headless)
options.add_argument('--headless=new')
# initializing webdriver for Chrome with our options
driver = webdriver.Chrome(options=options)

def printscreen(url, filename):
    try:
        driver.get(url)
        print("Page URL:", driver.current_url)
        print("Page Title:", driver.title)

        # set the window size
        pageWidth = driver.execute_script("return document.body.parentNode.scrollWidth")
        pageHeight = driver.execute_script("return document.body.parentNode.scrollHeight")

        # sometimes the page width is too big
        # so we need to limit the width
        if (pageWidth > 1920):
            pageWidth =  1920
            driver.set_window_size(pageWidth, pageHeight)
            pageHeight = driver.execute_script("return document.body.parentNode.scrollHeight")

        driver.set_window_size(pageWidth, pageHeight + 140)

        print("Window size:", driver.get_window_size())
        # save the screenshot
        driver.save_screenshot(filename)
        print("Screenshot saved")

    except Exception as e:
        print("Exception occurred " + repr(e))

def save_all_images(url, filename):
    # sendRequest
    response = requests.get(url)
    # Analyze HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Get all picture tags
    img_tags = soup.find_all("img")

    # Extract picture link
    img_urls = [urljoin(url, img["src"]) for img in img_tags]

    print("Found {} images".format(len(img_urls)))

    # Write the picture link to the file
    with open(filename, "a") as f:
        f.write("\n".join(img_urls) + "\n")

def get_all_links(url, paths = None, limit = 100):
    print("Crawling URL:", url)
    if paths is None:
        paths = set([url])
        yield url

    # get all links by tag name
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'a')
    hrefs = list(map(lambda link: link.get_attribute('href'), links))
    # cache the links to crawl next
    nextLevelLinks = []

    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)

    for href in hrefs:
        # transform relative url to absolute url
        absolute_url = urljoin(url, href)

        # check if the absolute_url is in the same domain
        # check if the url is not already in the list
        if domain in absolute_url and absolute_url not in paths:
            if len(paths) > limit:
                break
            paths.add(absolute_url)
            nextLevelLinks.append(absolute_url)
            yield absolute_url
    
    for link in nextLevelLinks:
        if len(paths) > limit:
            break
        yield from get_all_links(link, paths, limit)

@click.command()
@click.option('--url', default="https://www.gov.cn/zhengce/pdfFile/downloadFile.htm", help='Enter the URL you want.')
def save_website_screenshots(url):
    # create a folder for the domain
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    if os.path.exists(domain):
       domain = domain + "-" + str(uuid.uuid1())
    os.mkdir(domain)

    folder_path = os.path.join(os.getcwd(), domain)
    
    for link in get_all_links(url):
        # if the link is not html, write it to resources.txt
        _, suffix  = os.path.splitext(link)
        if suffix not in [".html", ".htm"] and suffix != "" :
            with open(folder_path + "/resources.txt", "a") as f:
                f.write(link + "\n")
            continue

        # create filename from path
        parsed_uri = urlparse(link)
        path = '{uri.path}'.format(uri=parsed_uri)
        filename = folder_path + "/" + quote(path, safe='') + ".png"

        printscreen(link, filename)
        save_all_images(link, folder_path + "/resources.txt")