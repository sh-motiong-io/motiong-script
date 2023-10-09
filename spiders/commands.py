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

        # click on 2015 for movie list of films
        driver.find_element(By.ID, '2015').click()
        film_titles = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'film-title')))

        for film_title in film_titles:
            print(film_title.text)

    except Exception as e:
        print("Exception occurred " + repr(e))

    finally:
        driver.close()
