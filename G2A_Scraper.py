import time
import dotenv
import json
import re
import os
import logging
from custom_functions.mailersend_funcs import send_email
from custom_functions.scrapping_funcs import scrape_site,scrape_site_pages,extract_data
from custom_functions.openai_funcs import makeHTMLTable


dotenv.load_dotenv()
MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')
MAILERSEND_FROM= os.getenv('MAILERSEND_FROM')
MAILERSEND_FROM_NAME= os.getenv('MAILERSEND_FROM_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_Config = os.getenv('OPENAI_CONFIG_LOCATION')
G2A_CONFIG_LOCATION = os.getenv('G2A_CONFIG_LOCATION')
SELENIUM_IMPLICIT_WAIT_TIME = os.getenv('SELENIUM_IMPLICIT_WAIT_TIME')
TIMER_WAIT_TIME= os.getenv('TIMER_WAIT_TIME')


def loadConfig(config_location:str):
    try:
        with open(config_location, 'r') as conf:
            return json.load(conf)
    except FileNotFoundError:
        return None

def extract_g2a_urls(config:list):
    urls = []
    for product in config['products']:
        urls.append(product['product_link'])
    return urls

def start_scraping_process(g2a_config,oi_config,urls:list,mode:str='single'):
    try:
        page_data = []
        if(mode == 'single'):
            page_data=scrape_site(urls[0],10,10)


        elif(mode == 'multi'):
            page_data=(scrape_site_pages(urls))


        else:
            print("Invalid mode")
            return None
        if(len(page_data) == 1):
           # soup = BeautifulSoup(page_data[0], 'html.parser')
            for product in g2a_config['products']:
                section = page_data
                #re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer-sc'))[0].text)
               #convert to string

                section = str(section)
                with open('test2.txt', 'w') as f:
                    f.write(section)
                section = str(extract_data(section))
                with open('test.txt', 'w') as f:
                    f.write(section)
                #html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config,product['product_name'],product['product_link'],product['minimum_seller_rating'],product['max_price'],product['max_results'])
                #send_email(MAILERSEND_FROM,MAILERSEND_FROM_NAME,product['mailing_list'],product['product_name'],"",html_table,MAILERSEND_API_KEY)
        elif(len(page_data) > 1):
            product = g2a_config['products']

            for i in range(len(urls)):# the order of the page_data should match the order of the urls so i can use the index to get the correct url
                #soup = BeautifulSoup(page_data[i], 'html.parser')

               # section =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer'))[0].text)
               # html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config,product[i]['product_name'],urls[i],product[i]['minimum_seller_rating'],product[i]['max_price'],product[i]['max_results'])
               # send_email(MAILERSEND_FROM,MAILERSEND_FROM_NAME,product[i]['mailing_list'],product[i]['product_name'],"",html_table,MAILERSEND_API_KEY)
                section = page_data[i]


        else:
            print("No data was returned")
            return None


    except Exception as e:
        print(e)
        print("Error in the scraping process")
        return None



oi_config=loadConfig(OPENAI_Config)
g2a_config=loadConfig(G2A_CONFIG_LOCATION)

print('Starting scraping process...\n')

urls = extract_g2a_urls(g2a_config)

if(urls is None):
    print("No urls found in the config file")
    exit(1)
elif(len(urls) == 1):
    start_scraping_process(g2a_config,oi_config,urls,'single')
elif(len(urls) > 1):
    start_scraping_process(g2a_config,oi_config,urls,'multi')
else:
    print("There were no valid URLs in the config file")



print("Done")

