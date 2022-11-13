import requests
import pandas
import time
import random
import json

session = requests.Session()
header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36', "Referer" : "https://www1.nseindia.com/products/content/equities/equities/archieve_eq.htm"}
session.get('https://www.nseindia.com/get-quotes/equity?symbol=HDFCBANK', headers=header)
cookies = session.cookies.get_dict()
print("Cookies has been set")

def get_all_stock_symbols(filename='list.txt'):
    with open(filename) as f:
        return [symbol.strip() for symbol in f.read().split()]
    
def get_data_for(stock):
    # your code to get data and return
    stock_data_url = f"https://www.nseindia.com/api/quote-equity?symbol={stock}"
    response = session.get(stock_data_url,headers=header, cookies=cookies)
    if response.status_code == 200:
        response = response.json()
        
        data = {}
        data['Given Stock'] = stock
        if 'metadata' in response and 'symbol' in response['metadata']:
            data['Symbol'] = response['metadata']['symbol']
            data['ISIN'] = response['metadata']['isin']
            data['Status'] = response['metadata']['status']
            data['Date of Listing'] = response['metadata']['listingDate']
            data['Basic Industry'] = response['metadata']['industry']
            data['Sectoral Index'] = response['metadata']['pdSectorInd']
            data['Macro-Economic Sector'] = response['industryInfo']['macro']
            data['Sector'] = response['industryInfo']['sector']
            data['Industry'] = response['industryInfo']['industry']

        return data

    return {}    

data = []
i = 0;
for stock in list(dict.fromkeys(get_all_stock_symbols())):
    # if i == 5:
    #     break
    if i % 300 == 0: 
        session.get('https://www.nseindia.com/get-quotes/equity?symbol=HDFCBANK', headers=header)
        cookies = session.cookies.get_dict()
        print("Cookies has been set")
    i += 1
    # time.sleep(random.random())
    data.append(get_data_for(stock))
    print(f"writing stock {i} {stock}")
df = pandas.DataFrame(data)
df.to_csv('nse_data_file.csv')
print(df)