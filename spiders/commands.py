import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@click.command()
@click.option('--url', default="https://www.motiong.com/", help='Enter the URL you want.')
def printscreen(url):
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

        # set the window size
        pageWidth = driver.execute_script("return document.body.parentNode.scrollWidth")
        pageHeight = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(pageWidth, pageHeight + 150)

        # save the screenshot
        # todo: save to a specific folder
        driver.save_screenshot("capture.png")

    except Exception as e:
        print("Exception occurred " + repr(e))

    finally:
        driver.close()