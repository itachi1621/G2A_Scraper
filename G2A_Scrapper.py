import time
import dotenv
import json
import re
import os
import logging
from bs4 import BeautifulSoup
from custom_functions.mailersend_funcs import send_email
from custom_functions.scrapping_funcs import scrape_site
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


def loadConfig(config_location):
    try:
        with open(config_location, 'r') as conf:
            return json.load(conf)
    except FileNotFoundError:
        return None

oi_config=loadConfig(OPENAI_Config)
g2a_config=loadConfig(G2A_CONFIG_LOCATION)

for product in g2a_config['products']:
    #g2a_config=g2a_config['products'][0]
    #print(g2a_config['product_link'])

    try:
        page_data = scrape_site(product['product_link'])
        #Remember to rewrite this later to be more efficient for multiple sites currently it will launch a headless browser for each product
        #Ill probably need to rewrite this block to be a function that returns the page_data for each product type


        soup = BeautifulSoup(page_data, 'html.parser')

        # now we need to use re to filter down to the section with the ul class id of  indexes__StyledOffersListItemContainer... that loosely matches that name
        #section = soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer'))[0].prettify()

        #now to get the seller ratings prices etc as text then we can use re to filter out the unwanted text
        # https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string see this link for the re.sub

        section =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer'))[0].text)
        html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config,product['product_name'],product['product_link'],product['minimum_seller_rating'],product['max_price'],product['max_results'])
        #print(html_table)
        send_email(MAILERSEND_FROM,MAILERSEND_FROM_NAME,product['mailing_list'],product['product_name'],"",html_table,MAILERSEND_API_KEY)
    except Exception as e:
        print(e)
        continue



print("Done")

