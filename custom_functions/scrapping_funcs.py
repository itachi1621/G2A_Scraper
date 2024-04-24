from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import re

def scrape_site(url:str,implicit_wait_time:int=10,timer_wait_time:int=5,retry_limit:int=3,is_retry:bool=False):
    try:
        if not is_retry:
            user_agent = UserAgent()
            options = Options()
            options.add_argument('-headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            options.add_argument(f'user-agent={user_agent.random}')
            options.page_load_strategy = 'none'
            driver = webdriver.Chrome(options=options)

        page_data = []
        if is_retry is True and retry_limit == 0:
            driver.quit()
            return None

        driver.implicitly_wait(implicit_wait_time)
        driver.get(url)
        time.sleep(timer_wait_time)

        soup = BeautifulSoup(page_data[0], 'html.parser')
        data =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer-sc'))[0].text)
        if(not isProductCheck(data)):
            print('Data not found retrying')
            driver.delete_all_cookies()
            scrape_site(url,implicit_wait_time,timer_wait_time,retry_limit-1,True)
        elif(isProductCheck):


            page_data.append(driver.page_source)
            driver.quit()
            return page_data

    except Exception as e:
        print(e)
        return None
def scrape_site_pages(urls:list,implicit_wait_time:int=10,timer_wait_time:int=5):
    try:
        user_agent = UserAgent()
        options = Options()
        options.add_argument('-headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        options.add_argument(f'user-agent={user_agent.random}')
        options.page_load_strategy = 'none'
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(implicit_wait_time)
        page_data = []
        for url in urls:
            driver.get(url)
            time.sleep(timer_wait_time)
            page_data.append(driver.page_source)
            #clear data
            driver.delete_all_cookies() #g2a was blocking after the first page :( so i had to clear the cookies from last request before making next one




        driver.quit()
        return page_data

    except Exception as e:
        print(e)
        driver.quit()
        return None


def extract_data(data):
    sellers = []
    for line in data.split('\n'):
        if line.strip():  # Skip empty lines
            parts = line.split('Positive feedback')
            seller_rating_str = parts[0].split()[-1].strip('%')
            seller_name = ' '.join(parts[0].split()[:-1]).strip()

            try:
                rating = int(seller_rating_str)
            except ValueError:
                rating = None  # If rating cannot be converted to int, set it to None

            prices = []
            for price_line in parts[1:]:
                price_data = price_line.split('$')[1:]
                discounted_price = float(price_data[0].strip())
                regular_price = float(price_data[1].split('-')[0].strip())
                prices.append({'discounted_price': discounted_price, 'regular_price': regular_price})

            sellers.append({'seller_name': seller_name, 'rating': rating, 'prices': prices})

    return sellers

def isProductCheck(data): #So turns out that the data doesn't always contain the word Positive feedback or add to cart mabee its an anti scraping measure so this is my anti anti scraping measure
   #need to check if data containd the word Positve feedback or  add to cart
   magic_words = ['Positive feedback','add to cart']
   if any(word in data for word in magic_words):
       return True
   else:
       return False

sample_data = """
Gamehive97%400Buyers'
feedback (last 12 months)37613View commentsAsk about the product
This seller does not issue invoices.Seller's store$ 7.13
Boings90%491Buyers' feedback (last 12 months)42749View commentsAsk about the productThis seller does not issue invoices.Seller's store$ 7.13WeWestgaming94%520Buyers' feedback (last 12 months)48331View commentsAsk about the productThis seller does not issue invoices.Seller's store$ 7.45Digitaldistribucion78%1297Buyers' feedback (last 12 months)988271View commentsAsk about the productThis seller issues invoices.Seller's store$ 8.32Leveluplegends96%393Buyers' feedback (last 12 months)31313View commentsAsk about the productThis seller does not issue invoices.Seller's store$ 8.62AmAmanda_game94%628Buyers' feedback (last 12 months)58037View commentsAsk about the productThis seller does not issue invoices.Seller's store$ 10.89Lordofstorms99%5677Buyers' feedback (last 12 months)526029View commentsAsk about the productExcellent sellerThis seller has received exceptionally high ratings from buyers for outstanding customer service.This seller does not issue invoices.Seller's store$ 11.55
"""

print(isProductCheck(sample_data))

