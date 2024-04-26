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

def start_scraping_process(g2a_config,oi_config,mode:str='single'):
    try:
        page_data = []
        if(mode == 'single'):
            page_data=scrape_site(g2a_config,10,5)


        elif(mode == 'multi'):
            page_data=(scrape_site_pages(g2a_config,10,5))


        else:
            print("Invalid mode")
            return None

        product_size = len(page_data['products'])
        if(product_size == 1 and mode == 'single'):
            #check if product_data is in the page_data
            if 'product_data' not in page_data['products'][0]:
                print("No product data was found")
                return None
           # print (page_data['products'][0]['product_data'])
           # soup = BeautifulSoup(page_data[0], 'html.parser')
            #conver to json string
            section =   str(page_data['products'][0]['product_data'])
            #print(section)
            #section =
            #page_data['products'][0]['product_data']
            html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config,page_data['products'][0])
            #print(html_table)
            send_email(MAILERSEND_FROM,MAILERSEND_FROM_NAME,page_data['products'][0]['mailing_list'],page_data['products'][0]['product_name'] ,"",html_table,MAILERSEND_API_KEY)
            """ if( result == "202" or result == "200"):
                print("Email sent successfully")
            else:
                print("Email failed to send")
                print(result) """
        elif(product_size >=1 and mode == 'multi'):
           # product = g2a_config['products']

            for i in range(product_size):# the order of the page_data should match the order of the urls so i can use the index to get the correct url
                #soup = BeautifulSoup(page_data[i], 'html.parser')
               section = str(page_data['products'][i]['product_data'])
               # section =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer'))[0].text)

               html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config,page_data['products'][i])
               print("Sending Email " + str(i+1) + " of " + str(product_size))
               send_email(MAILERSEND_FROM,MAILERSEND_FROM_NAME,page_data['products'][i]['mailing_list'],page_data['products'][i]['product_name'] ,"",html_table,MAILERSEND_API_KEY)
            """  if( result == "202" or result == "200"):
                print("Email sent successfully")
                continue
            else:
                print("Email failed to send")
                print(result)
                continue """


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

#urls = extract_g2a_urls(g2a_config)
number_of_products = len(g2a_config['products'])

if(number_of_products == 1):
    start_scraping_process(g2a_config,oi_config,'single')
elif(number_of_products > 1):
    start_scraping_process(g2a_config,oi_config,'multi')
else:
    print("There was an error in the config file")


print("Done")

