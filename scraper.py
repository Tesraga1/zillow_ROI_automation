import requests
from bs4 import BeautifulSoup
import json

headers = {
        "Accept": "*/*",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Cookie": "zjs_user_id=null",
    }

"""
    @parameters: link, a string address to a property's homedetails page
    @effect: Creates json file that contains a specified property's homedetails page
    @returns: none
    @modifies: none
    @throws: none

    Scrape data for a property and return a json file containing its information. 
    The file isn't created if the information isn't correctly gotten from the webpage
"""
def scrape_property_from_page(link: str):
    r = requests.get(link, headers=headers)

    if r.status_code == 200:
        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html5lib')
        #with open("output1.html", "w", encoding='utf-8') as file:
            #file.write(str(soup))
        #print(soup.prettify())
        data = soup.find(id="__NEXT_DATA__")
        with open("output1.html", "w", encoding='utf-8') as file:
            file.write(str(data.contents[0]))
        data = get_data(data)
        print(data["price"])
    else:
        print("Get request failed")
    print(r.status_code)

def get_data(data) -> dict[str, any]:
    d = json.loads(data.contents[0])
    property_data = json.loads(d["props"]["pageProps"]["componentProps"]["gdpClientCache"])
    property_data = property_data[list(property_data)[0]]['property']
    with open("output1.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(property_data, indent=2))
    return property_data

scrape_property_from_page('https://www.zillow.com/homedetails/883-Zittrouer-Rd-Guyton-GA-31312/105230722_zpid/')