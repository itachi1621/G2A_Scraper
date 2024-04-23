# G2A Product Scraper and Email Notifier

This Python script scrapes product information from G2A, extracts pricing, ratings, and seller names, creates an HTML table using ChatGPT, and sends email notifications to recipients specified in the configuration file.

## Prerequisites

- Python 3.x
- Required Python packages (install via `pip`):
  - `dotenv`
  - `bs4` (BeautifulSoup)
  - `requests`
  - `mailer-send`
  
## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/itachi1621/G2A_Scraper

2. Install Dependencies

   ```bash
   pip install -r requirements.txt

3. Create a .env file in the root directory and add the following environment variables: 
  ```plaintext
MAILERSEND_API_KEY=your_mailersend_api_key
MAILERSEND_FROM=your_email@domain.com
MAILERSEND_FROM_NAME=Your Name
OPENAI_API_KEY=your_openai_api_key
OPENAI_CONFIG_LOCATION=path_to_openai_config_file
G2A_CONFIG_LOCATION=path_to_g2a_config_file
SELENIUM_IMPLICIT_WAIT_TIME=your_selenium_implicit_wait_time
TIMER_WAIT_TIME=your_timer_wait_time
```

## Usage
Run the script.
```bash
python G2A_Scraper.py
```
## Configuration
- G2A Configuration File: Configure products and target prices in a JSON file.
- OpenAI Configuration File: Configure OpenAI settings in a JSON file.

## Custom Functions
- mailersend_funcs: Functions related to sending emails using MailerSend.
- scrapping_funcs: Functions for scraping websites.
- openai_funcs: Functions for interacting with OpenAI.

## Summary
1. Scraping Products from G2A:
  - The script scrapes product information from G2A, as defined in the g2a_config file.
2. Extracting Information:
  - It extracts pricing, ratings, and names of various sellers for each product.
3. HTML Table Creation:
  - Using ChatGPT, it creates an HTML table containing the scraped data.
4. Email Notification:
  - The script sends an email to recipients specified in the g2a_config file.
  - The email notifies recipients of items available around their target price.


