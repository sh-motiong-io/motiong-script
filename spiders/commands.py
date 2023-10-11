import os
from urllib.parse import urljoin, urlparse
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
        driver.set_window_size(pageWidth, pageHeight + 140)
        print("Window size:", driver.get_window_size())
        # save the screenshot
        # todo: save to a specific folder
        driver.save_screenshot(filename)
        print("Screenshot saved")

    except Exception as e:
        print("Exception occurred " + repr(e))

def get_all_links(url, paths = None):
    if paths is None:
        paths = set([url])
    elif len(paths) > 100:
        # accounts for more than 300 pages, stop crawling
        return paths

    # get all links by tag name
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'a')
    hrefs = list(map(lambda link: link.get_attribute('href'), links))

    for href in hrefs:
        # transform relative url to absolute url
        absolute_url = urljoin(url, href)

        # check if the url is in the same domain
        # check if the url is not already in the list
        if absolute_url.startswith(url) and absolute_url not in paths:
            paths.add(absolute_url)
            get_all_links(absolute_url, paths)
    return paths

@click.command()
@click.option('--url', default="https://www.motiong.com/", help='Enter the URL you want.')
def save_website_screenshots(url):
    links = get_all_links(url)

    # create a folder for the domain
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    if os.path.exists(domain):
       domain = domain + "-" + str(uuid.uuid1())
    os.mkdir(domain)

    folder_path = os.path.join(os.getcwd(), domain)
    
    for link in links:
        # create filename from path
        parsed_uri = urlparse(link)
        path = '{uri.path}'.format(uri=parsed_uri)
        filename = folder_path + "/" + path + ".png"

        printscreen(link, filename)