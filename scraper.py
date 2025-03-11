import requests
from bs4 import BeautifulSoup
import json
import random
import time
from utils import headers_list
headers = headers_list()

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
        data = get_singlepage_data(data)
        print(data["price"])
    else:
        print("Get request failed")
    print(r.status_code)

def get_singlepage_data(data) -> dict[str, any]:
    d = json.loads(data.contents[0])
    property_data = json.loads(d["props"]["pageProps"]["componentProps"]["gdpClientCache"])
    property_data = property_data[list(property_data)[0]]['property']
    with open("output1.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(property_data, indent=2))
    return property_data

def get_page_data(data) -> dict[str, any]:
    d = json.loads(data.contents[0])
    with open("output1.json", "w", encoding='utf-8') as file:
        file.write(str(d))
    print(d["props"]["pageProps"])
    property_data = json.loads(d["props"]["pageProps"])
    return property_data


def create_search_payload(
    query_data: dict, page_number: int = None
):
    """create a search payload for Zillow's search API"""
    payload = {
        "searchQueryState": query_data,
        "wants": {"cat1": ["listResults", "mapResults"], "cat2": ["total"]},
        "requestId": random.randint(2, 10),
    }
    if page_number:
        payload["searchQueryState"]["pagination"] = {"currentPage": page_number}
    return json.dumps(payload)


def search(location: str):
    page_info = []
    url = f"https://www.zillow.com/homes/{location}_rb/"
    h = headers[random.randint(0, len(headers)-1)]
    print(h)
    r = requests.get(url, headers=h)
    print(r.status_code)
    soup = BeautifulSoup(r.content, 'html5lib')
    data = soup.find(id="__NEXT_DATA__")
    data = json.loads(data.contents[0])
    d = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]
    page_info.append(d)
    numpages = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchList"]["totalPages"]
    queryState= data["props"]["pageProps"]["searchPageState"]["queryState"]
    
    for x in range(2, numpages + 1):
        time.sleep(0.01)
        h = headers[random.randint(0, len(headers)-1)]
        r = requests.put("https://www.zillow.com/async-create-search-page-state", headers=h, data=create_search_payload(queryState, x))
        print(r.status_code)
        if r.status_code != 200:
            continue
        r = r.json()
        r = r["cat1"]["searchResults"]["listResults"]
        page_info.append(r)
    return page_info

