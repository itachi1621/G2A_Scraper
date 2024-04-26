import requests
import time
def makeHTMLTable(html_data,open_ai_key=None,assistant_config=None,product_data:list=[]):


    table_title = product_data['product_name']
    table_link = product_data['product_link']
    minimum_seller_rating = product_data['minimum_seller_rating']
    max_price = product_data['max_price']
    max_results = product_data['max_results']




    #add the assistant config to the data message
   # data['messages'].append(assistant_config)
   #convert html data to safe string this means no ' or " in the string
    #html_data = html_data.replace('"',"'")


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
        data['messages'].append({"role": "user","content": "The title for this table is: "+table_title + " and the link for the site is: "+table_link+" please include it , the minimum seller rating  when making the table is: "+str(minimum_seller_rating)+"anything under that rating should be ignored"+" , the max price to be shown in the table is: "+str(max_price)+" the max results to be shown in this table is: "+str(max_results)})
        data['messages'].append({"role": "user","content":"include todays date in the html body with an h2 tag make it look nice, todays date is"+str(time.strftime("%Y-%m-%d"))})
        data['messages'].append({"role": "user","content": html_data})

        response = requests.Session()
        response = response.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']

        else:
            return response # Ill add in retry logic later
    except Exception as e:
        print(e)
        return e
