from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def scrape_site(url:str,implicit_wait_time:int=10,timer_wait_time:int=10):
    try:
        options = Options()
        options.add_argument('-headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        options.add_argument(f'user-agent={user_agent}')
        options.page_load_strategy = 'none'
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(implicit_wait_time)
        driver.get(url)

        time.sleep(timer_wait_time)
        page_data = driver.page_source


        #write all the data to a file

        driver.quit()
        return page_data

    except Exception as e:
        print(e)
        return None
