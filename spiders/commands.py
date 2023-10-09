import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@click.command()
@click.option('--url', default="https://www.motiong.com/", help='Enter the URL you want.')
def spider(url):
    # instance of Options class allows
    # us to configure Headless Chrome
    options = Options()

    # it should be run without UI (Headless)
    options.add_argument('--headless=new')

    # initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        print("Page URL:", driver.current_url)
        print("Page Title:", driver.title)
        
       # the method below is incorrect after testing
        # the pageheight is incorrect
        # todo: find a better way to get the page height
        pageWidth = driver.execute_script("return document.body.scrollWidth")
        pageHeight = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(pageWidth, pageHeight)

        driver.get_screenshot_as_file("capture.png")

    except Exception as e:
        print("Exception occurred " + repr(e))

    finally:
        driver.close()

spider()