from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import re

def scrape_site(g2a_config:list,implicit_wait_time:int=10,timer_wait_time:int=6,retry_limit:int=4):
    try:

        g2a_data = g2a_config.copy()

        for i in range(retry_limit):
            # Needed to start a whole new driver instance because the site may have some anti scrapping nonsense that prevents the driver from getting the data sometimes but not always
            user_agent = UserAgent()
            options = Options()
            #options.add_argument('-headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            options.add_argument(f'user-agent={user_agent.random}')
            options.page_load_strategy = 'none'
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(implicit_wait_time)
                #page_data = []
            url = g2a_data['products'][0]['product_link']
            #print(url)
            driver.get(url)
            time.sleep(timer_wait_time+retry_limit)

            soup =  BeautifulSoup(driver.page_source, 'html.parser')
            data =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer-sc'))[0].text)
           # print(data)
            isProduct= isProductCheck(data)
            if(not isProduct):
                print('Data not found retrying')
                driver.delete_all_cookies()
                #options.add_argument(f'user-agent={user_agent.random})')
                driver.quit()
                continue
            elif(isProduct):

                #page_data.append(data)
                g2a_data['products'][0]['product_data'] = data
                driver.quit()
                return g2a_config

        raise Exception("Couldn't retrieve data")

    except Exception as e:
        driver.quit()
        print(e)
        return None

def scrape_site_pages(g2a_config,implicit_wait_time:int=10,timer_wait_time:int=6,retry_limit:int=4):
    try:
        g2a_data = g2a_config.copy()
        for i in range(len(g2a_data['products'])):
            contained_product = False
            for j in range(retry_limit):
                # Needed to start a whole new driver instance because the site may have some anti scrapping nonsense that prevents the driver from getting the data sometimes but not always
                print("Try number: ",j+1)
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
                url = g2a_data['products'][i]['product_link']
                driver.get(url)
                time.sleep(timer_wait_time+retry_limit)

                soup =  BeautifulSoup(driver.page_source, 'html.parser')
                data =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer-sc'))[0].text)
                isProduct= isProductCheck(data)
                if(not isProduct):
                    print('Data not found retrying')
                    driver.delete_all_cookies()
                    driver.quit()
                    continue
                elif(isProduct):
                    g2a_data['products'][i]['product_data'] = data
                    contained_product = True
                    driver.quit()
                    break

        #if product data is not found in the page_data then lets remove it from the list
        if not contained_product:
            g2a_data['products'].pop(i)
            i -= 1

        return g2a_data
        #need to send i back by one so that the loop doesn't skip the next product pop will reindex


    except Exception as e:
        driver.quit()
        print(e)
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

