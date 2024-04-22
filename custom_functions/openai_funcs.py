import requests

def makeHTMLTable(html_data,open_ai_key=None,assistant_config=None,table_title:str="",table_link:str="",minimum_seller_rating:int=0,max_price:int=0,max_results:int=5):




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
        data['messages'].append({"role": "user","content": "The title for this table is: "+table_title + " and the link is: "+table_link+" and the minimum seller rating is: "+str(minimum_seller_rating)+" and the max price is: "+str(max_price)+" and the max results to be shown in this table is: "+str(max_results)})

        data['messages'].append({"role": "user","content": html_data})

        response = requests.Session()
        response = response.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']

        else:
            return response # Ill add in retry logic later
    except Exception as e:
        return e
