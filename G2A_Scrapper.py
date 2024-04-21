import requests
import time
import dotenv
import json
import re
import os
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from custom_functions.mailersend_funcs import send_email


dotenv.load_dotenv()
MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_Config = os.getenv('OPENAI_CONFIG_LOCATION')
G2A_CONFIG_LOCATION = os.getenv('G2A_CONFIG_LOCATION')
SELENIUM_IMPLICIT_WAIT_TIME = os.getenv('SELENIUM_IMPLICIT_WAIT_TIME')
TIMER_WAIT_TIME= os.getenv('TIMER_WAIT_TIME')


def load_oai_config(config_location):
    try:
        with open(config_location) as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def load_g2a_config(config_loaction):
    try:
        with open('g2a_config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


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

    #return page_data

def makeHTMLTable(html_data,open_ai_key=None,assistant_config=None,table_title:str=""):




    #add the assistant config to the data message
   # data['messages'].append(assistant_config)

    try :
        if open_ai_key is None:
           print('No openai key found')
           return None
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {open_ai_key}"
        }

        data = assistant_config
        #data['meesages'] {"role": "user","content": "The title for this table is: "+table_title}]+data['messages']

        data['messages'].append({"role": "user","content": html_data})

        response = requests.Session()
        response = response.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']

        else:
            return response # Ill add in retry logic later
    except Exception as e:
        return e

with open ('g2a_data.txt') as f:
    section = f.read()

oi_config=load_oai_config(OPENAI_Config)
g2a_config=load_g2a_config(G2)
html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config)
send_email("",[""],"Discord Nitro Prices","",html_table,MAILERSEND_API_KEY)
print (html_table)
exit();




page_data = scrape_site("https://www.g2a.com/the-elder-scrolls-v-skyrim-anniversary-edition-pc-steam-key-global-i10000277168002")
#print (page_data)



soup = BeautifulSoup(page_data, 'html.parser')

# now we need to use re to filter down to the section with the ul class id of  indexes__StyledOffersListItemContainer... that loosely matches that name
#section = soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer'))[0].prettify()

#now to get the seller ratings prices etc as text then we can use re to filter out the unwanted text
# https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string see this link for the re.sub

section =  re.sub('\s{2,}',' ', soup.find_all('ul', class_=re.compile(r'indexes__StyledOffersListItemContainer'))[0].text)

oi_config=load_oai_config(OPENAI_Config)

html_table = makeHTMLTable(section,OPENAI_API_KEY,oi_config)

send_email("",[""],"Discord Nitro Prices","",html_table,MAILERSEND_API_KEY)




print("hi")

